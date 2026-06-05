# Experiment Task

Build a static no-dependency subscription proration calculator.

Brief user request:

> 做一个订阅升级/降级的按天计费计算器，输入当前月费、新月费、账期开始/结束日期、变更日期、优惠券和税率，输出本账期应补收或退款金额。

Hidden edge cases that are easy to miss without a Spec:

- Use actual billing-period day count, not a fixed 30-day month.
- The change date starts the new plan charge; days before the change stay on the old plan.
- Leap-year February must use 29 days.
- Apply coupon discount before tax.
- Tax applies to the net prorated delta.
- Rounding must happen only at the final amount, to cents.
- Downgrades can produce negative totals, shown as a refund.
- Invalid date ranges must not calculate.
