import { useState } from "react";
import { CodeAnalysisForm } from "@/components/CodeAnalysisForm";
import { AnalysisResults } from "@/components/AnalysisResults";
import { LoadingState } from "@/components/LoadingState";
import { EmptyState } from "@/components/EmptyState";
import { ErrorState } from "@/components/ErrorState";
import { Code2, Sparkles } from "lucide-react";

export interface AnalysisResponse {
  explanation: string;
  suggestion: string;
  score: number;
  severity?: string;
  bug_type?: string;
  meta: {
    models_used: string[];
    per_model_latency_ms: Record<string, number>;
    total_latency_ms: number;
    had_repair: boolean;
    from_cache: boolean;
    backend_version?: string;
  };
}

const Index = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async (code: string, errorMessage: string, language?: string) => {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
      
      const response = await fetch(`${API_BASE_URL}/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          code,
          error_message: errorMessage,
          language,
        }),
      });

      if (!response.ok) {
        if (response.status === 400) {
          throw new Error('Invalid request. Please check your inputs.');
        } else if (response.status === 500) {
          throw new Error('Backend service error. Please try again later.');
        } else {
          throw new Error(`Error: ${response.status}`);
        }
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An unexpected error occurred. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-10">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center gap-3">
            <div className="relative">
              <Code2 className="h-8 w-8 text-primary" />
              <Sparkles className="h-4 w-4 text-accent absolute -top-1 -right-1" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-foreground">AI Code Assistant</h1>
              <p className="text-sm text-muted-foreground">Debug smarter with AI-powered explanations</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8 max-w-6xl">
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Left Column: Input Form */}
          <div className="space-y-6">
            <CodeAnalysisForm onAnalyze={handleAnalyze} isLoading={isLoading} onReset={handleReset} />
          </div>

          {/* Right Column: Results */}
          <div className="space-y-6">
            {isLoading && <LoadingState />}
            {!isLoading && !result && !error && <EmptyState />}
            {error && <ErrorState error={error} onRetry={handleReset} />}
            {result && !error && <AnalysisResults result={result} />}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-border mt-16 py-6">
        <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
          <p>Powered by multiple AI models for accurate bug detection and explanation</p>
        </div>
      </footer>
    </div>
  );
};

export default Index;
