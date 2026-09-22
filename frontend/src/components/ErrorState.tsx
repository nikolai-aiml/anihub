interface ErrorStateProps {
  title?: string;
  description?: string;
  onRetry?: () => void;
}

export function ErrorState({
  title = "Не удалось загрузить данные",
  description = "Попробуйте обновить страницу или повторить позже.",
  onRetry,
}: ErrorStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-20 px-6 text-center">
      <div className="w-20 h-20 rounded-3xl bg-red-500/10 border border-red-500/30 flex items-center justify-center mb-6 text-red-400 text-3xl">
        ✕
      </div>
      <h2 className="text-2xl font-bold font-display mb-3">{title}</h2>
      <p className="text-muted max-w-md mb-8">{description}</p>
      {onRetry && (
        <button onClick={onRetry} className="btn-primary">
          Попробовать снова
        </button>
      )}
    </div>
  );
}