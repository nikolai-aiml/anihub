import { useAuth } from "../contexts/AuthContext";

export function Profile() {
  const { user } = useAuth();
  if (!user) return null;

  const registeredAt = new Date(user.created_at).toLocaleDateString("ru-RU");

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <div className="card p-8">
        <div className="flex items-start gap-6">
          <div className="w-24 h-24 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center text-4xl font-bold">
            {user.username[0].toUpperCase()}
          </div>
          <div className="flex-1">
            <h1 className="text-3xl font-bold">{user.username}</h1>
            <p className="text-muted mt-1">{user.email}</p>
            {user.bio && <p className="mt-4">{user.bio}</p>}
            <p className="text-sm text-muted mt-4">
              Зарегистрирован: {registeredAt}
            </p>
          </div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-8 pt-8 border-t border-border">
          {[
            { label: "Смотрю", value: 0 },
            { label: "Просмотрено", value: 0 },
            { label: "В планах", value: 0 },
            { label: "Эпизодов", value: 0 },
          ].map((stat) => (
            <div key={stat.label} className="text-center">
              <div className="text-3xl font-bold text-primary">{stat.value}</div>
              <div className="text-sm text-muted mt-1">{stat.label}</div>
            </div>
          ))}
        </div>

        <p className="text-sm text-muted text-center mt-6">
          Статистика появится после добавления библиотеки
        </p>
      </div>
    </div>
  );
}