import { useEffect, useRef, useState } from "react";

export function HeroBackground() {
  const containerRef = useRef<HTMLDivElement>(null);
  const [mouse, setMouse] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!containerRef.current) return;
      const rect = containerRef.current.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width - 0.5) * 2;
      const y = ((e.clientY - rect.top) / rect.height - 0.5) * 2;
      setMouse({ x, y });
    };
    window.addEventListener("mousemove", handleMouseMove);
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, []);

  return (
    <div
      ref={containerRef}
      className="absolute inset-0 overflow-hidden pointer-events-none"
    >
      {/* ФОН — параллакс + лёгкий зум. Виден полностью. */}
      <div
        className="absolute inset-[-10%] bg-cover bg-center"
        style={{
          backgroundImage: "url('/background.jpg')",
          transform: `translate(${mouse.x * -50}px, ${mouse.y * -50}px) scale(1.15)`,
          transition: "transform 0.5s ease-out",
          animation: "slowZoom 12s ease-in-out infinite",
        }}
      />

      {/* ЛУНА — умеренная, чуть пульсирует */}
      <div
        className="absolute"
        style={{
          width: "250px",
          height: "250px",
          top: "10%",
          right: "15%",
          background:
            "radial-gradient(circle, rgba(255, 250, 230, 0.5) 0%, rgba(255, 230, 180, 0.2) 30%, transparent 70%)",
          transform: `translate(${mouse.x * 60}px, ${mouse.y * 60}px)`,
          transition: "transform 0.7s ease-out",
          animation: "moonPulse 5s ease-in-out infinite",
          filter: "blur(15px)",
        }}
      />

      {/* ТУМАН — лёгкий, полупрозрачный */}
      <div
        className="absolute inset-0"
        style={{
          background:
            "radial-gradient(ellipse at 25% 75%, rgba(120, 140, 200, 0.25) 0%, transparent 50%)",
          animation: "fogDrift 20s ease-in-out infinite",
          mixBlendMode: "screen",
        }}
      />

      {/* ТУМАН 2 — второй слой */}
      <div
        className="absolute inset-0"
        style={{
          background:
            "radial-gradient(ellipse at 75% 65%, rgba(150, 100, 180, 0.2) 0%, transparent 45%)",
          animation: "fogDrift 30s ease-in-out infinite reverse",
          mixBlendMode: "screen",
        }}
      />

      {/* ОГНИ — 3 точки, лёгкое мерцание */}
      <div
        className="absolute inset-0"
        style={{
          background: `
            radial-gradient(circle 12px at 15% 80%, rgba(255, 200, 100, 0.4) 0%, transparent 100%),
            radial-gradient(circle 15px at 40% 85%, rgba(255, 220, 120, 0.35) 0%, transparent 100%),
            radial-gradient(circle 10px at 70% 82%, rgba(255, 200, 100, 0.3) 0%, transparent 100%)
          `,
          animation: "flicker 3s ease-in-out infinite",
          mixBlendMode: "screen",
        }}
      />

      {/* Оверлей — умеренный, чтобы картинка читалась */}
      <div className="absolute inset-0 bg-bg/40" />
    </div>
  );
}