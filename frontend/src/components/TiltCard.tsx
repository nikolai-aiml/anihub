import { useRef, useState, type ReactNode } from "react";

interface TiltCardProps {
  children: ReactNode;
  className?: string;
  delay?: number;
}

export function TiltCard({ children, className = "", delay = 0 }: TiltCardProps) {
  const cardRef = useRef<HTMLDivElement>(null);
  const [transform, setTransform] = useState("");
  const [glowPosition, setGlowPosition] = useState({ x: 0, y: 0 });
  const [isHovered, setIsHovered] = useState(false);

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!cardRef.current) return;
    const rect = cardRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    // Tilt 2-4 градуса
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;
    const rotateX = ((y - centerY) / centerY) * -3;
    const rotateY = ((x - centerX) / centerX) * 3;

    setTransform(
      `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-8px) scale(1.02)`
    );
    setGlowPosition({ x, y });
  };

  const handleMouseLeave = () => {
    setTransform("");
    setIsHovered(false);
  };

  return (
    <div
      ref={cardRef}
      className={`group relative p-8 rounded-3xl glass-strong transition-all duration-500 cursor-pointer overflow-hidden ${className}`}
      style={{
        transform,
        transformStyle: "preserve-3d",
        transition: isHovered
          ? "transform 0.15s ease-out, box-shadow 0.4s ease"
          : "transform 0.6s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.4s ease",
        animation: `fadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) ${delay}ms both`,
      }}
      onMouseMove={handleMouseMove}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={handleMouseLeave}
    >
      {/* Световое пятно за курсором */}
      {isHovered && (
        <div
          className="absolute pointer-events-none"
          style={{
            left: glowPosition.x,
            top: glowPosition.y,
            transform: "translate(-50%, -50%)",
            width: "300px",
            height: "300px",
            background:
              "radial-gradient(circle, rgba(139,92,246,0.25) 0%, transparent 60%)",
            filter: "blur(40px)",
            transition: "opacity 0.3s ease",
          }}
        />
      )}

      {/* Внутреннее свечение по границе */}
      <div
        className="absolute inset-0 rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"
        style={{
          background:
            "radial-gradient(600px circle at var(--mouse-x, 50%) var(--mouse-y, 50%), rgba(139,92,246,0.1), transparent 40%)",
          border: "1px solid rgba(139,92,246,0.3)",
        }}
      />

      <div className="relative z-10">{children}</div>
    </div>
  );
}