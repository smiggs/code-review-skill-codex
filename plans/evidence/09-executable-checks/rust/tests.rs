use super::*;
use std::{
    cell::Cell,
    future::{poll_fn, Future},
    pin::Pin,
    rc::Rc,
    sync::{
        atomic::{AtomicBool, Ordering},
        Arc,
    },
    task::{Context, Poll},
    time::Duration,
};
use tokio::{
    io::{AsyncRead, AsyncReadExt, ReadBuf},
    sync::oneshot,
    time::timeout,
};

struct Controlled {
    data: &'static [u8],
    pos: usize,
    split: usize,
    open: Rc<Cell<bool>>,
}
impl AsyncRead for Controlled {
    fn poll_read(
        mut self: Pin<&mut Self>,
        _: &mut Context<'_>,
        buf: &mut ReadBuf<'_>,
    ) -> Poll<std::io::Result<()>> {
        if self.pos >= self.split && !self.open.get() {
            return Poll::Pending;
        }
        let end = if self.open.get() {
            self.data.len()
        } else {
            self.split.min(self.data.len())
        };
        let n = (end - self.pos).min(buf.remaining());
        buf.put_slice(&self.data[self.pos..self.pos + n]);
        self.pos += n;
        Poll::Ready(Ok(()))
    }
}
fn reader(data: &'static [u8], split: usize) -> (Controlled, Rc<Cell<bool>>) {
    let open = Rc::new(Cell::new(false));
    (
        Controlled {
            data,
            pos: 0,
            split,
            open: open.clone(),
        },
        open,
    )
}
async fn pending_once<F: Future>(future: Pin<&mut F>) {
    let mut future = future;
    poll_fn(|cx| {
        assert!(future.as_mut().poll(cx).is_pending());
        Poll::Ready(())
    })
    .await;
}

#[test]
fn valid_ownership_bounds_and_panic_invariant() {
    let input = String::from("borrowed");
    let parser = Parser { input: &input };
    assert_eq!(parser.input, "borrowed");
    assert_eq!(built_in_port(), 8080);
    assert_eq!(checked_byte(&[], 0), None);
    assert_eq!(checked_byte(&[8], 1), None);
    assert_eq!(checked_byte(&[8], usize::MAX), None);
    assert_eq!(checked_byte(&[8], 0), Some(8));
    // SAFETY: Index zero exists in this one-byte slice.
    assert_eq!(unsafe { unchecked_byte(&[8], 0) }, 8);
    let mut s = String::with_capacity(64);
    s.push_str("a");
    let ptr = s.as_ptr();
    let s = s + "b";
    assert_eq!(s, "ab");
    assert_eq!(s.as_ptr(), ptr);
}

#[tokio::test]
async fn partial_frame_survives_cancellation() {
    let (mut reader, open) = reader(b"abcdefgh", 2);
    let mut state = FourBytes::default();
    let mut first = Box::pin(state.read(&mut reader));
    pending_once(first.as_mut()).await;
    drop(first);
    open.set(true);
    assert_eq!(
        timeout(Duration::from_secs(2), state.read(&mut reader))
            .await
            .unwrap()
            .unwrap(),
        *b"abcd"
    );
    assert_eq!(state.read(&mut reader).await.unwrap(), *b"efgh");
}

#[tokio::test]
async fn frame_eof_is_an_error() {
    let (mut reader, open) = reader(b"ab", 2);
    open.set(true);
    let err = FourBytes::default().read(&mut reader).await.unwrap_err();
    assert_eq!(err.kind(), std::io::ErrorKind::UnexpectedEof);
}

#[tokio::test]
async fn losing_single_read_consumes_nothing() {
    let (mut reader, open) = reader(b"abcd", 0);
    let mut bytes = [0; 4];
    tokio::select! {
        biased;
        _ = reader.read(&mut bytes) => panic!("closed gate should stay pending"),
        _ = std::future::ready(()) => {}
    }
    open.set(true);
    assert_eq!(reader.read(&mut bytes).await.unwrap(), 4);
    assert_eq!(&bytes, b"abcd");
}

#[tokio::test]
async fn restarting_read_exact_loses_frame_alignment() {
    let (mut reader, open) = reader(b"abcdef", 2);
    let mut bytes = [0; 4];
    let mut first = Box::pin(reader.read_exact(&mut bytes));
    pending_once(first.as_mut()).await;
    drop(first);
    open.set(true);
    reader.read_exact(&mut bytes).await.unwrap();
    assert_eq!(&bytes, b"cdef");
}

#[tokio::test]
async fn pinned_read_exact_can_resume_same_future() {
    let (mut reader, open) = reader(b"abcd", 2);
    let mut bytes = [0; 4];
    let mut first = Box::pin(reader.read_exact(&mut bytes));
    pending_once(first.as_mut()).await;
    open.set(true);
    first.await.unwrap();
    assert_eq!(&bytes, b"abcd");
}

struct Dropped(Arc<AtomicBool>);
impl Drop for Dropped {
    fn drop(&mut self) {
        self.0.store(true, Ordering::SeqCst);
    }
}

#[tokio::test]
async fn abort_and_join_observes_destructors() {
    let dropped = Arc::new(AtomicBool::new(false));
    let flag = dropped.clone();
    let (tx, rx) = oneshot::channel();
    let handle = tokio::spawn(async move {
        let _guard = Dropped(flag);
        tx.send(()).unwrap();
        std::future::pending::<()>().await;
    });
    timeout(Duration::from_secs(2), rx).await.unwrap().unwrap();
    let failures = timeout(Duration::from_secs(2), stop_tasks(vec![handle]))
        .await
        .unwrap();
    assert_eq!(failures.len(), 1);
    assert!(failures[0].is_cancelled());
    assert!(dropped.load(Ordering::SeqCst));
    assert!(stop_tasks(Vec::new()).await.is_empty());
}

#[tokio::test]
async fn dropping_handle_detaches_work() {
    let (release, wait) = oneshot::channel();
    let (finished, done) = oneshot::channel();
    let handle = tokio::spawn(async move {
        wait.await.unwrap();
        finished.send(()).unwrap();
    });
    drop(handle);
    release.send(()).unwrap();
    timeout(Duration::from_secs(2), done)
        .await
        .unwrap()
        .unwrap();
}

#[tokio::test]
async fn started_blocking_work_ignores_abort() {
    let (start, started) = oneshot::channel();
    let (release, wait) = std::sync::mpsc::channel();
    let handle = tokio::task::spawn_blocking(move || {
        start.send(()).unwrap();
        wait.recv_timeout(Duration::from_secs(2)).unwrap();
        17
    });
    timeout(Duration::from_secs(2), started)
        .await
        .unwrap()
        .unwrap();
    handle.abort();
    release.send(()).unwrap();
    assert_eq!(
        timeout(Duration::from_secs(2), handle)
            .await
            .unwrap()
            .unwrap(),
        17
    );
}

#[tokio::test]
async fn join_failure_and_inner_error_are_distinct() {
    let inner = tokio::spawn(async { Err::<(), _>("failure") });
    assert_eq!(inner.await.unwrap(), Err("failure"));
    let panic = tokio::spawn(async { panic!("intentional panic control") });
    assert!(panic.await.unwrap_err().is_panic());
}
