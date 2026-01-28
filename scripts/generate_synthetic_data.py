import numpy as np
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta
from pathlib import Path


"""
Generate synthetic but realistic SaaS growth data for FlowPulse.

Tables:
- marketing_channels
- customers
- subscriptions
- payments
- user_events

Output CSVs are written to data/raw/.
"""

np.random.seed(42)
faker = Faker()

BASE_DATE_START = datetime(2023, 1, 1)
BASE_DATE_END = datetime(2025, 12, 31)


def generate_customers(n_customers: int = 40000) -> pd.DataFrame:
    """Simulate customer signups, segments, acquisition channels, and churn."""
    signup_dates = [
        faker.date_between(BASE_DATE_START, BASE_DATE_END) for _ in range(n_customers)
    ]

    countries = np.random.choice(
        ["US", "UK", "CA", "DE", "IN", "AU"],
        size=n_customers,
        p=[0.4, 0.15, 0.1, 0.1, 0.15, 0.1],
    )
    device_types = np.random.choice(
        ["web", "ios", "android"], size=n_customers, p=[0.4, 0.3, 0.3]
    )
    segments = np.random.choice(
        ["freelancer", "startup_employee", "enterprise_employee", "student"],
        size=n_customers,
        p=[0.35, 0.3, 0.2, 0.15],
    )

    # map to marketing_channels (will have 12 rows: 2 campaigns * 6 channels)
    acquisition_channel_ids = np.random.choice(range(1, 13), size=n_customers)

    customers = pd.DataFrame(
        {
            "customer_id": range(1, n_customers + 1),
            "signup_date": signup_dates,
            "country": countries,
            "device_type": device_types,
            "segment": segments,
            "acquisition_channel_id": acquisition_channel_ids,
        }
    )

    # Churn: ~35% overall, with random churn date after signup
    churn_flags = np.random.binomial(1, 0.35, size=n_customers)
    churn_offsets = np.random.randint(30, 600, size=n_customers)  # days after signup

    churn_dates = []
    for sd, offset, flag in zip(
        customers["signup_date"], churn_offsets, churn_flags
    ):
        if flag == 1:
            churn_date = sd + timedelta(days=int(offset))
            churn_date = min(churn_date, BASE_DATE_END.date())
            churn_dates.append(churn_date)
        else:
            churn_dates.append(pd.NaT)

    customers["churned_date"] = churn_dates
    customers["is_active"] = customers["churned_date"].isna()

    return customers


def generate_marketing_channels() -> pd.DataFrame:
    """Create a small set of acquisition channels and campaigns with CAC."""
    rows = []
    channels = [
        ("facebook_ads", 50),
        ("google_ads", 60),
        ("tiktok_ads", 40),
        ("seo", 25),
        ("referral", 15),
        ("partnerships", 70),
    ]
    channel_id = 1
    for name, base_cac in channels:
        for i in range(1, 3):  # 2 campaigns per channel
            rows.append(
                {
                    "channel_id": channel_id,
                    "channel_name": name,
                    "campaign_name": f"{name}_campaign_{i}",
                    "utm_medium": "cpc" if "ads" in name else "organic",
                    "utm_source": name.split("_")[0],
                    "cac_usd": float(base_cac + np.random.normal(0, 5)),
                }
            )
            channel_id += 1
    return pd.DataFrame(rows)


def generate_subscriptions(customers_df: pd.DataFrame) -> pd.DataFrame:
    """Create subscription lifecycles (free + paid tiers) per customer."""
    rows = []
    subs_counter = 1

    for _, row in customers_df.iterrows():
        plan = np.random.choice(
            ["free", "basic", "pro", "team"],
            p=[0.4, 0.3, 0.2, 0.1],
        )

        # Free-only users: one "free" subscription from signup to churn (or open-ended)
        if plan == "free":
            churn_reason = (
                np.random.choice(
                    ["not_using", "price", "competitor", "technical", None],
                    p=[0.25, 0.1, 0.1, 0.05, 0.5],
                )
                if pd.notna(row.churned_date)
                else None
            )

            rows.append(
                {
                    "subscription_id": subs_counter,
                    "customer_id": row.customer_id,
                    "plan_name": "free",
                    "subscription_start_date": row.signup_date,
                    "subscription_end_date": row.churned_date,
                    "is_active": pd.isna(row.churned_date),
                    "billing_period": "monthly",
                    "trial_start_date": pd.NaT,
                    "trial_end_date": pd.NaT,
                    "churn_reason": churn_reason,
                }
            )
            subs_counter += 1
            continue

        # Trial then paid
        trial_start = row.signup_date
        trial_end = trial_start + timedelta(days=14)
        churned = row.churned_date

        churn_reason = (
            np.random.choice(
                ["not_using", "price", "competitor", "technical", None],
                p=[0.25, 0.2, 0.1, 0.05, 0.4],
            )
            if pd.notna(churned)
            else None
        )

        rows.append(
            {
                "subscription_id": subs_counter,
                "customer_id": row.customer_id,
                "plan_name": plan,
                "subscription_start_date": trial_end,
                "subscription_end_date": churned,
                "is_active": pd.isna(churned),
                "billing_period": "monthly",
                "trial_start_date": trial_start,
                "trial_end_date": trial_end,
                "churn_reason": churn_reason,
            }
        )
        subs_counter += 1

    return pd.DataFrame(rows)


def plan_price(plan_name: str) -> int:
    """Return monthly plan price in USD."""
    mapping = {"free": 0, "basic": 9, "pro": 19, "team": 49}
    return mapping.get(plan_name, 0)


def generate_payments(subs_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate recurring payments for paid subscriptions.

    - Monthly billing cadence.
    - Some payments fail or are refunded (revenue leakage).
    """
    rows = []
    pay_id = 1

    for _, s in subs_df.iterrows():
        if s.plan_name == "free":
            continue

        start = pd.to_datetime(s.subscription_start_date)
        end = (
            pd.to_datetime(s.subscription_end_date)
            if pd.notna(s.subscription_end_date)
            else BASE_DATE_END
        )

        current = start
        while current <= end:
            base_amount = plan_price(s.plan_name)
            status = np.random.choice(
                ["success", "failed", "refunded"],
                p=[0.9, 0.07, 0.03],
            )
            amount = 0 if status in {"failed", "refunded"} else base_amount

            rows.append(
                {
                    "payment_id": pay_id,
                    "subscription_id": s.subscription_id,
                    "payment_date": current.date(),
                    "amount_usd": float(amount),
                    "payment_status": status,
                    "payment_method": np.random.choice(
                        ["card", "paypal", "apple_pay", "google_pay"]
                    ),
                    "invoice_id": f"INV-{s.subscription_id}-{current.strftime('%Y%m')}",
                    "is_renewal": True,
                }
            )
            pay_id += 1

            # move roughly one month ahead
            current = current + timedelta(days=30)

    return pd.DataFrame(rows)


def generate_user_events(
    customers_df: pd.DataFrame, avg_events_per_user: int = 40
) -> pd.DataFrame:
    """
    Generate product usage events with engagement signals.

    - Active users have more events and longer tails.
    - Includes logins, tasks, reminders, plan changes, cancellations.
    """
    rows = []
    event_id = 1
    event_types = [
        "signup",
        "login",
        "task_created",
        "task_completed",
        "reminder_set",
        "plan_upgraded",
        "plan_downgraded",
        "subscription_canceled",
    ]

    for _, c in customers_df.iterrows():
        base_events = max(5, int(np.random.poisson(avg_events_per_user)))
        if c.is_active:
            base_events += np.random.randint(10, 40)
        else:
            base_events -= np.random.randint(0, 10)

        n_events = max(5, base_events)

        signup = pd.to_datetime(c.signup_date)
        end_date = (
            pd.to_datetime(c.churned_date)
            if pd.notna(c.churned_date)
            else BASE_DATE_END
        )

        for _ in range(n_events):
            event_day = faker.date_between(signup, end_date)
            etype = np.random.choice(
                event_types,
                p=[0.02, 0.3, 0.25, 0.25, 0.1, 0.03, 0.03, 0.02],
            )
            rows.append(
                {
                    "event_id": event_id,
                    "customer_id": c.customer_id,
                    "event_timestamp": event_day,
                    "event_type": etype,
                    "device_type": c.device_type,
                    "plan_name_at_event": np.random.choice(
                        ["free", "basic", "pro", "team"]
                    ),
                    "session_id": faker.uuid4(),
                }
            )
            event_id += 1

    return pd.DataFrame(rows)


def main() -> None:
    """Entry point: generate all tables and write to data/raw/."""
    out_dir = Path("data/raw")
    out_dir.mkdir(parents=True, exist_ok=True)

    marketing = generate_marketing_channels()
    customers = generate_customers()
    subscriptions = generate_subscriptions(customers)
    payments = generate_payments(subscriptions)
    events = generate_user_events(customers)

    marketing.to_csv(out_dir / "marketing_channels.csv", index=False)
    customers.to_csv(out_dir / "customers.csv", index=False)
    subscriptions.to_csv(out_dir / "subscriptions.csv", index=False)
    payments.to_csv(out_dir / "payments.csv", index=False)
    events.to_csv(out_dir / "user_events.csv", index=False)

    print("Synthetic data written to data/raw/")


if __name__ == "__main__":
    main()

