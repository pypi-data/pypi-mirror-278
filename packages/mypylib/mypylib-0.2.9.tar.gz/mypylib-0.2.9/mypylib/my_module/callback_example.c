#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <time.h>

typedef void (*callback_t)(const char*);

pthread_t thread;
callback_t global_callback;

void* thread_func(void* arg) {
    char buffer[100];
    while (1) {
        time_t now = time(NULL);
        struct tm* t = localtime(&now);
        strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", t);
        global_callback(buffer);
        sleep(1);
    }
    return NULL;
}

void start_thread(callback_t callback) {
    global_callback = callback;
    pthread_create(&thread, NULL, thread_func, NULL);
}

void stop_thread() {
    pthread_cancel(thread);
    pthread_join(thread, NULL);
}

