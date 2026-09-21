import { useState } from "react";
import { StarIcon } from "./icons";

interface StarRatingProps {
  value: number | null;
  onChange: (value: number) => void;
  onRemove?: () => void;
  disabled?: boolean;
  size?: "sm" | "md" | "lg";
  max?: number;
}

const SIZES = {
  sm: "w-4 h-4",
  md: "w-6 h-6",
  lg: "w-8 h-8",
};

export function StarRating({
  value,
  onChange,
  onRemove,
  disabled = false,
  size = "md",
  max = 10,
}: StarRatingProps) {
  const [hovered, setHovered] = useState<number | null>(null);

  const displayValue = hovered ?? value ?? 0;

  return (
    <div className="flex items-center gap-2">
      <div
        className="flex items-center gap-1"
        onMouseLeave={() => setHovered(null)}
      >
        {Array.from({ length: max }, (_, i) => i + 1).map((star) => {
          const isFilled = star <= displayValue;
          return (
            <button
              key={star}
              type="button"
              disabled={disabled}
              onClick={() => onChange(star)}
              onMouseEnter={() => !disabled && setHovered(star)}
              className={`
                transition-all duration-150
                ${disabled ? "cursor-not-allowed opacity-50" : "cursor-pointer hover:scale-110"}
                ${isFilled ? "text-yellow-400" : "text-gray-600"}
              `}
              aria-label={`Оценка ${star} из ${max}`}
            >
              <StarIcon className={SIZES[size]} filled={isFilled} />
            </button>
          );
        })}
      </div>

      {displayValue > 0 && (
        <span
          className={`
            font-bold tabular-nums
            ${size === "lg" ? "text-2xl" : size === "md" ? "text-lg" : "text-sm"}
            text-yellow-400
          `}
        >
          {displayValue}
          <span className="text-gray-500 font-normal">/{max}</span>
        </span>
      )}

      {value !== null && onRemove && !disabled && (
        <button
          type="button"
          onClick={onRemove}
          className="ml-2 text-xs text-muted hover:text-red-400 transition-colors"
        >
          Удалить
        </button>
      )}
    </div>
  );
}