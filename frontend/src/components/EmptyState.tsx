import type { ReactNode } from "react";
import { Link } from "react-router-dom";
import { ArrowRightIcon } from "./icons";

interface EmptyStateProps {
  icon: ReactNode;
  title: string;
  description?: string;
  actionLabel?: string;
  actionTo?: string;
  onAction?: () => void;
}

export function EmptyState({
  icon,
  title,
  description,
  actionLabel,
  actionTo,
  onAction,
}: EmptyStateProps) {
  const action = actionTo ? (
    <Link
      to={actionTo}
      className="btn-primary inline-flex items-center gap-2"
    >
      {actionLabel}
      <ArrowRightIcon className="w-4 h-4" />
    </Link>
  ) : onAction ? (
    <button onClick={onAction} className="btn-primary">
      {actionLabel}
    </button>
  ) : null;

  return (
    <div className="flex flex-col items-center justify-center py-20 px-6 text-center animate-fade-in">
      <div className="w-20 h-20 rounded-3xl bg-primary/10 border border-primary/20 flex items-center justify-center mb-6 text-primary">
        {icon}
      </div>
      <h2 className="text-2xl font-bold font-display mb-3">{title}</h2>
      {description && (
        <p className="text-muted max-w-md mb-8 leading-relaxed">{description}</p>
      )}
      {action}
    </div>
  );
}