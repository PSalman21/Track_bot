import pandas as pd


def generate_insights(rows):

    if not rows or len(rows) < 3:
        return (
            "Недостаточно данных для аналитики.\n"
            "Добавь хотя бы 3 записи."
        )

    df = pd.DataFrame(
        rows,
        columns=[
            "date",
            "mood",
            "work",
            "sleep",
            "comment"
        ]
    )

    insights = []

    avg_mood = round(df["mood"].mean(), 2)
    avg_sleep = round(df["sleep"].mean(), 2)
    avg_work = round(df["work"].mean(), 2)

    insights.append(
        f"Среднее настроение: {avg_mood}"
    )

    insights.append(
        f"Средний сон: {avg_sleep} ч"
    )

    insights.append(
        f"Средняя работа: {avg_work} ч"
    )

    sleep_corr = df["sleep"].corr(df["mood"])
    work_corr = df["work"].corr(df["mood"])

    if sleep_corr > 0.3:
        insights.append(
            "Чем больше ты спишь — тем лучше настроение."
        )

    elif sleep_corr < -0.3:
        insights.append(
            "Большой сон связан с ухудшением настроения."
        )

    else:
        insights.append(
            "Сон слабо влияет на настроение."
        )

    if work_corr < -0.3:
        insights.append(
            "Долгая работа может ухудшать настроение."
        )

    elif work_corr > 0.3:
        insights.append(
            "Продуктивность улучшает настроение."
        )

    best_day = df.loc[df["mood"].idxmax()]

    insights.append(
        f" Лучший день:\n"
        f"{best_day['date']} "
        f"(настроение {best_day['mood']})"
    )

    return "\n\n".join(insights)