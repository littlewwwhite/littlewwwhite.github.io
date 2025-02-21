#!/bin/bash

# 检查是否安装了必要的 Python 包
check_dependencies() {
    echo "检查依赖..."
    pip install openai python-dotenv pyyaml > /dev/null 2>&1
}

# 显示菜单
show_menu() {
    echo "博客工具菜单："
    echo "1. 优化博客内容"
    echo "2. 优化并生成博客元数据"
    echo "3. 仅格式化博客开头结构"
    echo "4. 完整处理（先优化内容，再生成元数据）"
    echo "5. 退出"
    echo
    read -p "请选择操作 (1-5): " choice
}

# 获取文章名称
get_post_name() {
    read -p "请输入文章名称（输入 'all' 处理所有文章）: " post_name
    echo $post_name
}

# 主程序
main() {
    check_dependencies

    while true; do
        show_menu
        case $choice in
            1)
                post_name=$(get_post_name)
                python3 tools/blog_optimizer.py "$post_name"
                ;;
            2)
                post_name=$(get_post_name)
                python3 tools/blog_processor.py "$post_name"
                ;;
            3)
                post_name=$(get_post_name)
                python3 tools/blog_formatter.py "$post_name"
                ;;
            4)
                post_name=$(get_post_name)
                echo "开始优化内容..."
                python3 tools/blog_optimizer.py "$post_name"
                echo "开始生成元数据..."
                python3 tools/blog_processor.py "$post_name"
                ;;
            5)
                echo "退出程序"
                exit 0
                ;;
            *)
                echo "无效的选择，请重试"
                ;;
        esac
        echo
        read -p "按回车键继续..."
    done
}

# 运行主程序
main
