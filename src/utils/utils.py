from datetime import datetime, timedelta


def generate_semesters(start_date: str, end_date: str):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    semesters = []
    current = start

    while current < end:
        # First half: Jan–Jun
        if current.month == 1:
            next_sem = datetime(current.year, 7, 1)
            semesters.append((current.strftime("%Y-%m-%d"), (next_sem - timedelta(days=1)).strftime("%Y-%m-%d")))
            current = next_sem

        # Second half: Jul–Dec
        elif current.month == 7:
            next_sem = datetime(current.year, 12, 31)
            semesters.append((current.strftime("%Y-%m-%d"), next_sem.strftime("%Y-%m-%d")))
            current = datetime(current.year + 1, 1, 1)

    return semesters