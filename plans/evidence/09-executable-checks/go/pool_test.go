package audit

import (
	"context"
	"errors"
	"fmt"
	"sync"
	"sync/atomic"
	"testing"
	"time"
)

func bounded(t *testing.T, f func() error) error {
	t.Helper()
	done := make(chan error, 1)
	go func() { done <- f() }()
	select {
	case err := <-done:
		return err
	case <-time.After(2 * time.Second):
		t.Fatal("operation did not terminate")
		return nil
	}
}

func TestWorkerBoundaries(t *testing.T) {
	for _, n := range []int{-1, 0} {
		for _, items := range [][]int{nil, {1}} {
			if bounded(t, func() error {
				return ProcessAll(context.Background(), items, n, func(context.Context, int) error { t.Error("invalid input invoked callback"); return nil })
			}) == nil {
				t.Fatalf("workers=%d accepted", n)
			}
		}
	}
	if err := ProcessAll(context.Background(), nil, 1, nil); err != nil {
		t.Fatal(err)
	}
	ctx, cancel := context.WithCancel(context.Background())
	cancel()
	if !errors.Is(ProcessAll(ctx, nil, 1, nil), context.Canceled) {
		t.Fatal("cancelled empty input accepted")
	}
	if !errors.Is(ProcessAll(ctx, []int{1}, 1, func(context.Context, int) error { t.Error("pre-cancelled callback"); return nil }), context.Canceled) {
		t.Fatal("pre-cancelled work accepted")
	}
}

func TestCompletesEveryItemAndJoins(t *testing.T) {
	var mu sync.Mutex
	seen := make(map[int]int)
	var active atomic.Int32
	err := bounded(t, func() error {
		return ProcessAll(context.Background(), []int{1, 2, 3, 4}, 20, func(_ context.Context, i int) error {
			active.Add(1)
			defer active.Add(-1)
			mu.Lock()
			seen[i]++
			mu.Unlock()
			return nil
		})
	})
	if err != nil || active.Load() != 0 {
		t.Fatalf("return=%v active=%d", err, active.Load())
	}
	for i := 1; i <= 4; i++ {
		if seen[i] != 1 {
			t.Fatalf("item %d processed %d times", i, seen[i])
		}
	}
}

func TestCancellationAndBound(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	started := make(chan struct{}, 2)
	var active, maximum atomic.Int32
	done := make(chan error, 1)
	go func() {
		done <- ProcessAll(ctx, []int{1, 2, 3, 4, 5}, 2, func(ctx context.Context, _ int) error {
			n := active.Add(1)
			defer active.Add(-1)
			for old := maximum.Load(); n > old && !maximum.CompareAndSwap(old, n); old = maximum.Load() {
			}
			started <- struct{}{}
			<-ctx.Done()
			return ctx.Err()
		})
	}()
	for i := 0; i < 2; i++ {
		select {
		case <-started:
		case <-time.After(2 * time.Second):
			t.Fatal("workers did not start")
		}
	}
	cancel()
	if err := bounded(t, func() error { return <-done }); !errors.Is(err, context.Canceled) {
		t.Fatal(err)
	}
	if active.Load() != 0 || maximum.Load() != 2 {
		t.Fatalf("active=%d maximum=%d", active.Load(), maximum.Load())
	}
}

func TestCallbackFailureCancelsSiblingAndJoins(t *testing.T) {
	sibling := make(chan struct{})
	failure := errors.New("failed")
	var active atomic.Int32
	err := bounded(t, func() error {
		return ProcessAll(context.Background(), []int{1, 2, 3}, 2, func(ctx context.Context, i int) error {
			active.Add(1)
			defer active.Add(-1)
			if i == 1 {
				<-sibling
				return failure
			}
			if i == 2 {
				close(sibling)
				<-ctx.Done()
				return ctx.Err()
			}
			t.Error("unexpected later work")
			return nil
		})
	})
	if !errors.Is(err, failure) || active.Load() != 0 {
		t.Fatalf("err=%v active=%d", err, active.Load())
	}
}

func TestNonpositiveNonemptyTerminates(t *testing.T) {
	for _, n := range []int{-1, 0} {
		t.Run(fmt.Sprint(n), func(t *testing.T) {
			if err := bounded(t, func() error {
				return ProcessAll(context.Background(), []int{1}, n, func(context.Context, int) error { return nil })
			}); err == nil {
				t.Fatal("invalid worker count accepted")
			}
		})
	}
}

func TestDeadlineAndErrorIdentity(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 20*time.Millisecond)
	defer cancel()
	err := bounded(t, func() error {
		return ProcessAll(ctx, []int{1}, 1, func(ctx context.Context, _ int) error { <-ctx.Done(); return ctx.Err() })
	})
	if !errors.Is(err, context.DeadlineExceeded) {
		t.Fatal(err)
	}
}
