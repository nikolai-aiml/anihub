import { useState, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { useMutation } from "@tanstack/react-query";
import { authApi } from "../api/auth";
import { useAuth } from "../contexts/AuthContext";
import { useToast } from "../contexts/ToastContext";

export function Settings() {
  const { user, logout } = useAuth();
  const { showToast } = useToast();
  const navigate = useNavigate();

  const [profileForm, setProfileForm] = useState({
    username: user?.username ?? "",
    email: user?.email ?? "",
    bio: user?.bio ?? "",
    avatar_url: user?.avatar_url ?? "",
  });

  const [passwordForm, setPasswordForm] = useState({
    old_password: "",
    new_password: "",
    new_password_confirm: "",
  });

  const [showPassword, setShowPassword] = useState(false);

  // ============ ОБНОВЛЕНИЕ ПРОФИЛЯ ============
  const updateProfileMutation = useMutation({
    mutationFn: () =>
      authApi.updateMe({
        username: profileForm.username,
        email: profileForm.email,
        bio: profileForm.bio || null,
        avatar_url: profileForm.avatar_url || null,
      }),
    onSuccess: () => {
      showToast("Профиль обновлён", "success");
      // Перезагружаем страницу, чтобы AuthContext получил новые данные
      window.location.reload();
    },
    onError: (err: any) => {
      showToast(err.response?.data?.detail || "Ошибка", "error");
    },
  });

  // ============ СМЕНА ПАРОЛЯ ============
  const changePasswordMutation = useMutation({
    mutationFn: () => authApi.changePassword(passwordForm),
    onSuccess: () => {
      showToast("Пароль изменён", "success");
      setPasswordForm({
        old_password: "",
        new_password: "",
        new_password_confirm: "",
      });
    },
    onError: (err: any) => {
      showToast(err.response?.data?.detail || "Ошибка", "error");
    },
  });

  const handleProfileSubmit = (e: FormEvent) => {
    e.preventDefault();
    updateProfileMutation.mutate();
  };

  const handlePasswordSubmit = (e: FormEvent) => {
    e.preventDefault();

    if (passwordForm.new_password !== passwordForm.new_password_confirm) {
      showToast("Новые пароли не совпадают", "error");
      return;
    }
    if (passwordForm.new_password.length < 8) {
      showToast("Пароль должен быть минимум 8 символов", "error");
      return;
    }

    changePasswordMutation.mutate();
  };

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  if (!user) return null;

  return (
    <div className="container mx-auto px-6 py-8 max-w-2xl">
      <div className="mb-8">
        <h1 className="text-3xl font-bold font-display">Настройки</h1>
        <p className="text-muted text-sm mt-1">
          Управление аккаунтом и безопасностью
        </p>
      </div>

      {/* Секция 1: Профиль */}
      <div className="glass rounded-2xl p-6 border border-white/5 mb-6">
        <h2 className="text-xl font-bold font-display mb-6">Профиль</h2>

        <form onSubmit={handleProfileSubmit} className="space-y-4">
          <div>
            <label className="block text-sm text-gray-300 mb-2">
              Username
            </label>
            <input
              type="text"
              className="input"
              value={profileForm.username}
              onChange={(e) =>
                setProfileForm({ ...profileForm, username: e.target.value })
              }
              required
              minLength={3}
            />
          </div>

          <div>
            <label className="block text-sm text-gray-300 mb-2">Email</label>
            <input
              type="email"
              className="input"
              value={profileForm.email}
              onChange={(e) =>
                setProfileForm({ ...profileForm, email: e.target.value })
              }
              required
            />
          </div>

          <div>
            <label className="block text-sm text-gray-300 mb-2">
              Bio (о себе)
            </label>
            <textarea
              className="input resize-none"
              rows={3}
              maxLength={500}
              value={profileForm.bio}
              onChange={(e) =>
                setProfileForm({ ...profileForm, bio: e.target.value })
              }
              placeholder="Расскажи о себе..."
            />
          </div>

          <div>
            <label className="block text-sm text-gray-300 mb-2">
              Avatar URL
            </label>
            <input
              type="url"
              className="input"
              value={profileForm.avatar_url}
              onChange={(e) =>
                setProfileForm({ ...profileForm, avatar_url: e.target.value })
              }
              placeholder="https://example.com/avatar.png"
            />
          </div>

          <button
            type="submit"
            disabled={updateProfileMutation.isPending}
            className="btn-primary"
          >
            {updateProfileMutation.isPending ? "Сохранение..." : "Сохранить"}
          </button>
        </form>
      </div>

      {/* Секция 2: Смена пароля */}
      <div className="glass rounded-2xl p-6 border border-white/5 mb-6">
        <h2 className="text-xl font-bold font-display mb-6">Смена пароля</h2>

        <form onSubmit={handlePasswordSubmit} className="space-y-4">
          <div>
            <label className="block text-sm text-gray-300 mb-2">
              Текущий пароль
            </label>
            <input
              type={showPassword ? "text" : "password"}
              className="input"
              value={passwordForm.old_password}
              onChange={(e) =>
                setPasswordForm({
                  ...passwordForm,
                  old_password: e.target.value,
                })
              }
              required
            />
          </div>

          <div>
            <label className="block text-sm text-gray-300 mb-2">
              Новый пароль
            </label>
            <input
              type={showPassword ? "text" : "password"}
              className="input"
              value={passwordForm.new_password}
              onChange={(e) =>
                setPasswordForm({
                  ...passwordForm,
                  new_password: e.target.value,
                })
              }
              required
              minLength={8}
            />
          </div>

          <div>
            <label className="block text-sm text-gray-300 mb-2">
              Повторите новый пароль
            </label>
            <input
              type={showPassword ? "text" : "password"}
              className="input"
              value={passwordForm.new_password_confirm}
              onChange={(e) =>
                setPasswordForm({
                  ...passwordForm,
                  new_password_confirm: e.target.value,
                })
              }
              required
              minLength={8}
            />
          </div>

          <label className="flex items-center gap-2 text-sm text-muted cursor-pointer">
            <input
              type="checkbox"
              checked={showPassword}
              onChange={(e) => setShowPassword(e.target.checked)}
              className="w-4 h-4 rounded border-border bg-surface"
            />
            Показать пароли
          </label>

          <button
            type="submit"
            disabled={changePasswordMutation.isPending}
            className="btn-primary"
          >
            {changePasswordMutation.isPending
              ? "Изменение..."
              : "Изменить пароль"}
          </button>
        </form>
      </div>

      {/* Секция 3: Опасная зона */}
      <div className="glass rounded-2xl p-6 border border-red-500/30 bg-red-500/5">
        <h2 className="text-xl font-bold font-display mb-3 text-red-400">
          Опасная зона
        </h2>
        <p className="text-sm text-muted mb-4">
          Выйти из аккаунта на этом устройстве
        </p>
        <button onClick={handleLogout} className="btn-ghost text-red-400">
          Выйти из аккаунта
        </button>
      </div>
    </div>
  );
}