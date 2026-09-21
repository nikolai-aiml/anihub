import { useRef, useState, type ReactNode } from "react";

interface GlowButtonProps {
  children: ReactNode;
  onClick?: () => void;
  href?: string;
  variant?: "primary" | "ghost";
  className?: string;
}

export function GlowButton({
  children,
  onClick,
  href,
  variant = "primary",
  className = "",
}: GlowButtonProps) {
  const buttonRef = useRef<HTMLDivElement>(null);
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [isHovered, setIsHovered] = useState(false);

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!buttonRef.current) return;
    const rect = buttonRef.current.getBoundingClientRect();
    setPosition({
      x: e.clientX - rect.left,
      y: e.clientY - rect.top,
    });
  };

  const baseClasses =
    "relative inline-flex items-center justify-center gap-3 px-8 py-4 text-base md:text-lg font-semibold rounded-2xl overflow-hidden transition-all duration-500 group cursor-pointer";

  const variantClasses =
    variant === "primary"
      ? "text-white bg-gradient-to-r from-primary/90 via-primary to-primary-hover/90 shadow-xl shadow-primary/30 hover:shadow-2xl hover:shadow-primary/50 hover:scale-[1.03] active:scale-[0.98]"
      : "text-white glass-button hover:bg-primary/25 hover:border-primary/50 hover:shadow-lg hover:shadow-primary/20 hover:scale-[1.02] active:scale-[0.98]";

  const content = (
    <>
      {/* Световое пятно за курсором */}
      {isHovered && (
        <div
          className="absolute pointer-events-none transition-opacity duration-300"
          style={{
            left: position.x,
            top: position.y,
            transform: "translate(-50%, -50%)",
            width: "200px",
            height: "200px",
            background:
              variant === "primary"
                ? "radial-gradient(circle, rgba(255,255,255,0.25) 0%, transparent 60%)"
                : "radial-gradient(circle, rgba(139,92,246,0.4) 0%, transparent 60%)",
            filter: "blur(20px)",
          }}
        />
      )}

      {/* Градиентный фон для primary */}
      {variant === "primary" && (
        <div className="absolute inset-0 bg-gradient-to-r from-primary via-accent/80 to-primary bg-[length:200%_100%] opacity-0 group-hover:opacity-100 group-hover:animate-gradient-shift transition-opacity duration-500" />
      )}

      {/* Контент */}
      <span className="relative z-10 flex items-center gap-3">{children}</span>
    </>
  );

  if (href) {
    return (
      <a
        href={href}
        className={`${baseClasses} ${variantClasses} ${className}`}
        ref={buttonRef as any}
        onMouseMove={handleMouseMove}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
      >
        {content}
      </a>
    );
  }

  return (
    <div
      ref={buttonRef}
      onClick={onClick}
      className={`${baseClasses} ${variantClasses} ${className}`}
      onMouseMove={handleMouseMove}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {content}
    </div>
  );
}