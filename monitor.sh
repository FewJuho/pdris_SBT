#!/bin/bash

LOG_DIR="./logs"
mkdir -p "$LOG_DIR"

monitor_disk_usage() {
    current_date=""
    start_init=1
    log_file=$(date "+%Y-%m-%d %H:%M:%S")
    while true; do
        timestamp=$(date "+%Y-%m-%d %H:%M:%S")
        today=$(date "+%Y-%m-%d")

        # Создаем файл при смене даты и при перезапуске
        if [ "$today" != "$current_date" ] || [ $start_init -eq 1 ]; then
            log_file="$LOG_DIR/monitor_for_${timestamp}.csv"
            echo "timestamp,disk_usage,inodes_usage" > "$log_file"
            current_date="$today"
            start_init=0
        fi

        disk_usage=$(df / | awk 'NR==2 {print $5}')
        inodes_usage=$(df -i / | awk 'NR==2 {print $5}')

        echo "$timestamp,$disk_usage,$inodes_usage" >> "$log_file"

        sleep 10 #удобнее для тестирования
    done
}


start() {
    if [ -f monitor.pid ]; then
        echo "Процесс уже запущен. PID: $(cat monitor.pid)"
        exit 1
    fi

    monitor_disk_usage &

    echo $! > monitor.pid
    echo "Мониторинг запущен. PID: $!"
}

stop() {
    if [ ! -f monitor.pid ]; then
        echo "Процесс не запущен"
        exit 1
    fi

    pid=$(cat monitor.pid)
    kill $pid
    rm -f monitor.pid
    echo "Процесс остановлен"
}

status() {
    if [ -f monitor.pid ]; then
        echo "Процесс запущен. PID: $(cat monitor.pid)"
    else
        echo "Процесс не запущен"
    fi
}

case "$1" in
START)
    start
    ;;
STOP)
    stop
    ;;
STATUS)
    status
    ;;
*)
    echo "Usage: $0 {START|STOP|STATUS}"
    exit 1
    ;;
esac

