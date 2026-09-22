import { useRef, useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { AnimeCard } from "./AnimeCard";
import { ArrowRightIcon } from "./icons";
import { StaggerContainer, StaggerItem } from "./Stagger";
import type { AnimeListItem } from "../types";

interface AnimeCarouselProps {
  title: string;
  subtitle?: string;
  anime: AnimeListItem[];
  viewAllLink?: string;
}

export function AnimeCarousel({
  title,
  subtitle,
  anime,
  viewAllLink,
}: AnimeCarouselProps) {
  const scrollRef = useRef<HTMLDivElement>(null);
  const [isHovered, setIsHovered] = useState(false);

  // Блокируем scroll body при hover, компенсируя ширину скроллбара
  useEffect(() => {
    if (!isHovered) return;

    const scrollbarWidth =
      window.innerWidth - document.documentElement.clientWidth;

    const prevOverflow = document.body.style.overflow;
    const prevPaddingRight = document.body.style.paddingRight;

    document.body.style.overflow = "hidden";
    if (scrollbarWidth > 0) {
      document.body.style.paddingRight = `${scrollbarWidth}px`;
    }

    return () => {
      document.body.style.overflow = prevOverflow;
      document.body.style.paddingRight = prevPaddingRight;
    };
  }, [isHovered]);

  // Плавный scroll колёсиком через RAF
  useEffect(() => {
    const el = scrollRef.current;
    if (!el) return;

    let rafId: number | null = null;
    let targetScrollLeft = 0;

    const handleWheel = (e: WheelEvent) => {
      // Игнорируем, если есть горизонтальный скролл
      if (e.deltaX !== 0) return;
      if (e.deltaY === 0) return;

      if (rafId === null) {
        targetScrollLeft = el.scrollLeft;
      }

      targetScrollLeft += e.deltaY;

      const maxScroll = el.scrollWidth - el.clientWidth;
      targetScrollLeft = Math.max(0, Math.min(maxScroll, targetScrollLeft));

      if (rafId !== null) return;

      const smoothScroll = () => {
        const diff = targetScrollLeft - el.scrollLeft;
        if (Math.abs(diff) < 0.5) {
          el.scrollLeft = targetScrollLeft;
          rafId = null;
          return;
        }
        el.scrollLeft += diff * 0.2;   // 20% к цели за кадр
        rafId = requestAnimationFrame(smoothScroll);
      };

      rafId = requestAnimationFrame(smoothScroll);
    };

    el.addEventListener("wheel", handleWheel, { passive: true });

    return () => {
      el.removeEventListener("wheel", handleWheel);
      if (rafId !== null) cancelAnimationFrame(rafId);
    };
  }, []);

  if (anime.length === 0) return null;

  const scroll = (direction: "left" | "right") => {
    if (!scrollRef.current) return;
    const scrollAmount = direction === "left" ? -400 : 400;
    scrollRef.current.scrollBy({ left: scrollAmount, behavior: "smooth" });
  };

  return (
    <section className="mb-12">
      <div className="flex items-end justify-between mb-5">
        <div>
          <h2 className="text-2xl font-bold font-display">{title}</h2>
          {subtitle && <p className="text-sm text-muted mt-1">{subtitle}</p>}
        </div>

        <div className="flex items-center gap-2">
          {viewAllLink && (
            <Link
              to={viewAllLink}
              className="text-sm text-primary hover:text-primary-hover transition-colors inline-flex items-center gap-1"
            >
              Все
              <ArrowRightIcon className="w-4 h-4" />
            </Link>
          )}

          <div className="hidden md:flex gap-1">
            <button
              onClick={() => scroll("left")}
              className="w-8 h-8 rounded-lg glass-button flex items-center justify-center text-white hover:bg-primary/25 transition-colors"
              aria-label="Прокрутить влево"
            >
              ←
            </button>
            <button
              onClick={() => scroll("right")}
              className="w-8 h-8 rounded-lg glass-button flex items-center justify-center text-white hover:bg-primary/25 transition-colors"
              aria-label="Прокрутить вправо"
            >
              →
            </button>
          </div>
        </div>
      </div>

      <div
        ref={scrollRef}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
        className="flex gap-4 overflow-x-auto pb-3 scrollbar-hide"
        style={{
          scrollbarWidth: "none",
          msOverflowStyle: "none",
        }}
      >
        <StaggerContainer className="flex gap-4">
          {anime.map((item) => (
            <StaggerItem
              key={item.id}
              className="flex-shrink-0 w-[160px] sm:w-[180px]"
            >
              <AnimeCard anime={item} />
            </StaggerItem>
          ))}
        </StaggerContainer>
      </div>
    </section>
  );
}