from app import orders, processor, render_report

if __name__ == "__main__":
    render_report(processor(orders))
