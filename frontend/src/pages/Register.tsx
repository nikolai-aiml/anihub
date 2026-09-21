import { useState, type FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

export function Register() {
  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    passwordConfirm: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const { register } = useAuth();
  const navigate = useNavigate();

  const update = (field: string, value: string) =>
    setForm((prev) => ({ ...prev, [field]: value }));

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");

    if (form.password !== form.passwordConfirm) {
      setError("Пароли не совпадают");
      return;
    }

    setLoading(true);
    try {
      await register(form.username, form.email, form.password, form.passwordConfirm);
      navigate("/profile");
    } catch (err: any) {
      const detail = err.response?.data?.detail;
      setError(typeof detail === "string" ? detail : "Ошибка регистрации");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-md">
        <div className="card p-8">
          <h1 className="text-3xl font-bold mb-2">Регистрация</h1>
          <p className="text-muted mb-6">Создай новый аккаунт</p>

          {error && (
            <div className="mb-4 p-3 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400 text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm mb-2">Username</label>
              <input
                type="text"
                className="input"
                value={form.username}
                onChange={(e) => update("username", e.target.value)}
                required
                minLength={3}
              />
            </div>
            <div>
              <label className="block text-sm mb-2">Email</label>
              <input
                type="email"
                className="input"
                value={form.email}
                onChange={(e) => update("email", e.target.value)}
                required
              />
            </div>
            <div>
              <label className="block text-sm mb-2">Пароль</label>
              <input
                type="password"
                className="input"
                value={form.password}
                onChange={(e) => update("password", e.target.value)}
                required
                minLength={8}
              />
            </div>
            <div>
              <label className="block text-sm mb-2">Повторите пароль</label>
              <input
                type="password"
                className="input"
                value={form.passwordConfirm}
                onChange={(e) => update("passwordConfirm", e.target.value)}
                required
                minLength={8}
              />
            </div>
            <button type="submit" disabled={loading} className="btn-primary w-full">
              {loading ? "Создание..." : "Создать аккаунт"}
            </button>
          </form>

          <p className="mt-6 text-sm text-muted text-center">
            Уже есть аккаунт?{" "}
            <Link to="/login" className="text-primary hover:underline">
              Войти
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}   