package audit

import (
	"errors"
	"fmt"
	"sync"
	"testing"
)

type sampleError struct{}

func (*sampleError) Error() string { return "sample" }

func TestErrorChainsAndTypedNil(t *testing.T) {
	var pointer *sampleError
	var err error = pointer
	if err == nil {
		t.Fatal("typed nil incorrectly treated as nil interface")
	}
	cause := &sampleError{}
	wrapped := fmt.Errorf("operation: %w", cause)
	var matched *sampleError
	if !errors.Is(wrapped, cause) || !errors.As(wrapped, &matched) || matched != cause {
		t.Fatal("lost wrapped cause")
	}
	if errors.Is(fmt.Errorf("operation: %v", cause), cause) {
		t.Fatal("format-only text wrapped the cause")
	}
}

func TestSharedSliceAndIndependentCopy(t *testing.T) {
	original := []int{1, 2, 3}
	shared := original[:1:1]
	shared[0] = 9
	if original[0] != 9 {
		t.Fatal("full slice expression isolated an element")
	}
	independent := make([]int, len(original))
	copy(independent, original)
	independent[0] = 7
	if original[0] != 9 {
		t.Fatal("copy still shares element storage")
	}
	appended := append(shared, 4)
	appended[0] = 6
	if original[0] != 9 {
		t.Fatal("capacity-limited append reused original array")
	}
}

func TestChannelCoordinatorClosesAfterSenders(t *testing.T) {
	ch := make(chan int)
	var wg sync.WaitGroup
	for i := 1; i <= 2; i++ {
		wg.Add(1)
		go func(n int) { defer wg.Done(); ch <- n }(i)
	}
	go func() { wg.Wait(); close(ch) }()
	total := 0
	if err := bounded(t, func() error {
		for n := range ch {
			total += n
		}
		return nil
	}); err != nil {
		t.Fatal(err)
	}
	if total != 3 {
		t.Fatal(total)
	}
	if value, ok := <-ch; value != 0 || ok {
		t.Fatalf("closed receive %d %v", value, ok)
	}
}
