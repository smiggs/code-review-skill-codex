use tokio::io::{self, AsyncRead, AsyncReadExt};

#[derive(Default)]
pub struct FourBytes {
    bytes: [u8; 4],
    filled: usize,
}

impl FourBytes {
    pub async fn read<R: AsyncRead + Unpin>(&mut self, reader: &mut R)
        -> io::Result<[u8; 4]>
    {
        self.filled = 0;
        while self.filled < self.bytes.len() {
            let n = reader.read(&mut self.bytes[self.filled..]).await?;
            if n == 0 {
                return Err(io::ErrorKind::UnexpectedEof.into());
            }
            self.filled += n;
        }
        self.filled = 0;
        Ok(self.bytes)
    }
}
