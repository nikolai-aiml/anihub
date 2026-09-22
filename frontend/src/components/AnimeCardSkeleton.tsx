export function AnimeCardSkeleton() {
  return (
    <div className="card animate-pulse">
      <div className="aspect-[2/3] bg-white/5" />
      <div className="p-3 space-y-2">
        <div className="h-4 bg-white/5 rounded w-full" />
        <div className="h-4 bg-white/5 rounded w-3/4" />
        <div className="h-3 bg-white/5 rounded w-1/2 mt-3" />
      </div>
    </div>
  );
}

export function AnimeGridSkeleton({ count = 20 }: { count?: number }) {
  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
      {Array.from({ length: count }, (_, i) => (
        <AnimeCardSkeleton key={i} />
      ))}
    </div>
  );
}