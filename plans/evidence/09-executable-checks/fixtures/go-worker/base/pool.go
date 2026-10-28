package audit

import (
    "context"
    "fmt"
    "sync"
)

func ProcessAll(parent context.Context, items []int, workers int,
    process func(context.Context, int) error) error {
    if workers <= 0 {
        return fmt.Errorf("workers must be positive: %d", workers)
    }
    if err := parent.Err(); err != nil {
        return err
    }
    if len(items) == 0 {
        return nil
    }
    if workers > len(items) {
        workers = len(items)
    }
    ctx, cancel := context.WithCancelCause(parent)
    defer cancel(nil)
    jobs := make(chan int)
    var wg sync.WaitGroup
    for w := 0; w < workers; w++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for {
                select {
                case <-ctx.Done():
                    return
                case item, ok := <-jobs:
                    if !ok || ctx.Err() != nil {
                        return
                    }
                    if err := process(ctx, item); err != nil {
                        cancel(fmt.Errorf("item %d: %w", item, err))
                        return
                    }
                }
            }
        }()
    }
feed:
    for _, item := range items {
        select {
        case <-ctx.Done():
            break feed
        case jobs <- item:
        }
    }
    close(jobs)
    wg.Wait()
    return context.Cause(ctx)
}
