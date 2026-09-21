import { useEffect, useState } from "react";

export function CursorGlow() {
  const [position, setPosition] = useState({ x: -100, y: -100 });

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setPosition({ x: e.clientX, y: e.clientY });
    };
    window.addEventListener("mousemove", handleMouseMove);
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, []);

  return (
    <div
      className="fixed pointer-events-none z-[9999] hidden md:block"
      style={{
        left: position.x,
        top: position.y,
        transform: "translate(-50%, -50%)",
        width: "400px",
        height: "400px",
        background:
          "radial-gradient(circle, rgba(139,92,246,0.08) 0%, transparent 50%)",
        filter: "blur(40px)",
        transition: "opacity 0.3s ease",
      }}
    />
  );
}