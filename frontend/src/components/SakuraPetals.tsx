import { useEffect, useState, useRef } from "react";
import { motion } from "framer-motion";

interface PetalData {
  id: number;
  xPercent: number;
  size: number;
  duration: number;
  delay: number;
  rotation: number;
  color: string;
  opacity: number;
  swayAmount: number;
  swayDuration: number;
}

const PETAL_COLORS = [
  "rgba(255, 183, 197, 0.85)",
  "rgba(255, 209, 220, 0.75)",
  "rgba(255, 160, 180, 0.9)",
  "rgba(255, 220, 230, 0.7)",
  "rgba(236, 72, 153, 0.6)",
];

const PETAL_COUNT = 20;

function generatePetals(): PetalData[] {
  return Array.from({ length: PETAL_COUNT }, (_, i) => ({
    id: i,
    xPercent: Math.random() * 100,
    size: 12 + Math.random() * 16,
    duration: 12 + Math.random() * 10,
    delay: Math.random() * 12,
    rotation: Math.random() * 360,
    color: PETAL_COLORS[Math.floor(Math.random() * PETAL_COLORS.length)],
    opacity: 0.5 + Math.random() * 0.4,
    swayAmount: 20 + Math.random() * 30,
    swayDuration: 4 + Math.random() * 4,
  }));
}

function PetalSVG({ color, size }: { color: string; size: number }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      style={{ filter: "drop-shadow(0 2px 4px rgba(255, 150, 180, 0.3))" }}
    >
      <path
        d="M12 2C12 2 8 6 6 10C4 14 6 20 12 22C18 20 20 14 18 10C16 6 12 2 12 2Z"
        fill={color}
        stroke={color}
        strokeWidth="0.5"
      />
      <path
        d="M12 8C11 9 10 11 10 13C10 15 11 17 12 18"
        stroke="rgba(255,255,255,0.4)"
        strokeWidth="0.5"
        fill="none"
      />
    </svg>
  );
}

export function SakuraPetals() {
  const [petals] = useState<PetalData[]>(() => generatePetals());
  const [isMobile, setIsMobile] = useState(false);

  // Refs на DOM каждого лепестка
  const petalRefs = useRef<(HTMLDivElement | null)[]>([]);
  const wrapperRef = useRef<HTMLDivElement>(null);

  // Текущая и целевая позиции мыши (в refs — без ререндера!)
  const mouseXRef = useRef<number | null>(null);
  const currentMouseXRef = useRef<number | null>(null);

  // Мобильный
  useEffect(() => {
    const checkMobile = () => setIsMobile(window.innerWidth < 768);
    checkMobile();
    window.addEventListener("resize", checkMobile);
    return () => window.removeEventListener("resize", checkMobile);
  }, []);

  // Анимация через RAF — обновляем transform напрямую
  useEffect(() => {
    if (isMobile) return;

    const handleMouseMove = (e: MouseEvent) => {
      mouseXRef.current = e.clientX;
    };

    let rafId: number;

    const tick = () => {
      const target = mouseXRef.current;
      const current = currentMouseXRef.current;

      if (target !== null) {
        // Плавное сглаживание
        if (current === null) {
          currentMouseXRef.current = target;
        } else {
          currentMouseXRef.current = current + (target - current) * 0.08;
        }
        const smoothX = currentMouseXRef.current;

        // Обновляем transform КАЖДОГО лепестка напрямую — БЕЗ ререндера
        const windowWidth = window.innerWidth;
        const MAX_DISTANCE = 350;
        const MAX_OFFSET = 100;

        petalRefs.current.forEach((el, i) => {
          if (!el) return;
          const petal = petals[i];
          if (!petal) return;

          const petalPixelX = (petal.xPercent / 100) * windowWidth;
          const distance = Math.abs(smoothX - petalPixelX);

          let offsetX = 0;
          if (distance < MAX_DISTANCE) {
            const normalized = 1 - distance / MAX_DISTANCE;
            offsetX = normalized * normalized * MAX_OFFSET;
          }

          el.style.transform = `translateX(${offsetX}px)`;
        });
      }

      rafId = requestAnimationFrame(tick);
    };

    window.addEventListener("mousemove", handleMouseMove);
    rafId = requestAnimationFrame(tick);

    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      cancelAnimationFrame(rafId);
    };
  }, [isMobile, petals]);

  if (isMobile) return null;

  return (
    <div
      ref={wrapperRef}
      className="absolute inset-0 overflow-hidden pointer-events-none"
      style={{ zIndex: 1 }}
    >
      {petals.map((petal, i) => (
        <motion.div
          key={petal.id}
          className="absolute"
          style={{
            left: `${petal.xPercent}%`,
            top: 0,
            opacity: petal.opacity,
          }}
          initial={{ y: "-10vh" }}
          animate={{ y: "110vh" }}
          transition={{
            y: {
              duration: petal.duration,
              delay: petal.delay,
              repeat: Infinity,
              ease: "linear",
            },
          }}
        >
          <motion.div
            animate={{
              rotate: [petal.rotation, petal.rotation + 360],
              x: [0, petal.swayAmount, 0, -petal.swayAmount, 0],
            }}
            transition={{
              rotate: {
                duration: petal.duration * 0.8,
                repeat: Infinity,
                ease: "linear",
              },
              x: {
                duration: petal.swayDuration,
                repeat: Infinity,
                ease: "easeInOut",
              },
            }}
          >
            {/* Внешний div для ветра — обновляется через RAF */}
            <div
              ref={(el) => {
                petalRefs.current[i] = el;
              }}
              style={{
                willChange: "transform",
                transition: "transform 0.2s ease-out",
              }}
            >
              <PetalSVG color={petal.color} size={petal.size} />
            </div>
          </motion.div>
        </motion.div>
      ))}
    </div>
  );
}