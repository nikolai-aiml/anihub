import { Component, type ReactNode } from "react";

interface ErrorBoundaryProps {
  children: ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<
  ErrorBoundaryProps,
  ErrorBoundaryState
> {
  state: ErrorBoundaryState = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error) {
    console.error("ErrorBoundary caught:", error);
  }

  handleReload = () => {
    window.location.href = "/";
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center px-6">
          <div className="text-center max-w-md">
            <div className="text-7xl mb-6">💥</div>
            <h1 className="text-3xl font-bold font-display mb-3">
              Что-то пошло не так
            </h1>
            <p className="text-muted mb-8">
              Произошла непредвиденная ошибка. Попробуйте вернуться на главную.
            </p>
            <button onClick={this.handleReload} className="btn-primary">
              На главную
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}