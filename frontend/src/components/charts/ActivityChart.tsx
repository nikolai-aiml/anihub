import type { MonthActivity } from "../../types";

interface ActivityChartProps {
  activity: MonthActivity[];
}

const MONTH_NAMES = [
  "Янв", "Фев", "Мар", "Апр", "Май", "Июн",
  "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек",
];

function formatMonth(month: string): string {
  const [, m] = month.split("-");
  return MONTH_NAMES[parseInt(m, 10) - 1] || month;
}

export function ActivityChart({ activity }: ActivityChartProps) {
  if (activity.length === 0) {
    return (
      <div className="glass rounded-2xl p-6 border border-white/5">
        <h3 className="text-lg font-bold font-display mb-4">Активность</h3>
        <p className="text-muted text-sm text-center py-8">
          Начни оценивать аниме, чтобы увидеть активность
        </p>
      </div>
    );
  }

  const maxCount = Math.max(...activity.map((a) => a.count), 1);
  const CHART_HEIGHT = 160;

  return (
    <div className="glass rounded-2xl p-6 border border-white/5">
      <h3 className="text-lg font-bold font-display mb-6">Активность</h3>

      <div className="flex items-end justify-between gap-2 h-40">
        {activity.map((item) => {
          const height = (item.count / maxCount) * CHART_HEIGHT;
          return (
            <div
              key={item.month}
              className="flex-1 flex flex-col items-center gap-2 group"
            >
              <div className="text-xs text-muted tabular-nums opacity-0 group-hover:opacity-100 transition-opacity">
                {item.count}
              </div>
              <div
                className="w-full bg-gradient-to-t from-primary to-accent rounded-t-lg transition-all duration-700 hover:opacity-80"
                style={{ height: `${Math.max(height, 4)}px` }}
              />
              <div className="text-xs text-muted">
                {formatMonth(item.month)}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}