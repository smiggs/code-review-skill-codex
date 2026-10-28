package audit
import "context"
func ProcessAll(ctx context.Context, items []int, workers int, process func(context.Context,int) error) error {
    jobs := make(chan int, len(items))
    results := make(chan error, len(items))

    // 启动 worker
    for w := 0; w < workers; w++ {
        go func() {
            for item := range jobs {
                results <- process(ctx,item)
            }
        }()
    }

    // 发送任务
    for _, item := range items {
        jobs <- item
    }
    close(jobs)

    // 收集结果
    for range items {
        if err := <-results; err != nil {
            return err
        }
    }
    return nil
}
