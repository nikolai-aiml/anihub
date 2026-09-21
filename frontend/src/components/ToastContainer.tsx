import { useToast, type ToastType } from "../contexts/ToastContext";

const icons: Record<ToastType, string> = {
  success: "✓",
  error: "✕",
  info: "ℹ",
};

const colors: Record<ToastType, string> = {
  success: "border-green-500/40 text-green-400 bg-green-500/10",
  error: "border-red-500/40 text-red-400 bg-red-500/10",
  info: "border-primary/40 text-primary bg-primary/10",
};

export function ToastContainer() {
  const { toasts, removeToast } = useToast();

  return (
    <div className="fixed top-20 right-4 z-[100] flex flex-col gap-2 pointer-events-none">
      {toasts.map((toast) => (
        <div
          key={toast.id}
          onClick={() => removeToast(toast.id)}
          className={`
            pointer-events-auto cursor-pointer
            flex items-center gap-3 px-4 py-3 rounded-xl
            backdrop-blur-xl border shadow-2xl
            min-w-[280px] max-w-md
            animate-toast-in
            ${colors[toast.type]}
          `}
        >
          <span className="text-lg font-bold">{icons[toast.type]}</span>
          <span className="text-sm font-medium text-white flex-1">
            {toast.message}
          </span>
        </div>
      ))}
    </div>
  );
}