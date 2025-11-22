import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { MetadataSection } from "@/components/MetadataSection";
import { CheckCircle2, Lightbulb, AlertCircle, AlertTriangle, Bug } from "lucide-react";
import type { AnalysisResponse } from "@/pages/Index";

interface AnalysisResultsProps {
  result: AnalysisResponse;
}

export const AnalysisResults = ({ result }: AnalysisResultsProps) => {
  const getScoreColor = (score: number) => {
    if (score >= 80) return "text-success";
    if (score >= 50) return "text-warning";
    return "text-destructive";
  };

  const getScoreLabel = (score: number) => {
    if (score >= 80) return "High Confidence";
    if (score >= 50) return "Medium Confidence";
    return "Low Confidence";
  };

  const getSeverityVariant = (severity?: string) => {
    switch (severity?.toLowerCase()) {
      case "high":
        return "destructive";
      case "medium":
        return "default";
      case "low":
        return "secondary";
      default:
        return "outline";
    }
  };

  return (
    <div className="space-y-4 animate-in fade-in duration-500">
      {/* Success Header */}
      <div className="flex items-center gap-2 text-success">
        <CheckCircle2 className="h-5 w-5" />
        <span className="font-semibold">Analysis Complete</span>
      </div>

      {/* Explanation Section */}
      <Card className="p-6 bg-card border-border space-y-4">
        <div className="flex items-start gap-3">
          <div className="p-2 rounded-lg bg-primary/10">
            <AlertCircle className="h-5 w-5 text-primary" />
          </div>
          <div className="flex-1 space-y-2">
            <h3 className="font-semibold text-lg text-foreground">Root Cause Explanation</h3>
            <p className="text-muted-foreground leading-relaxed">{result.explanation}</p>
          </div>
        </div>
      </Card>

      {/* Suggestion Section */}
      <Card className="p-6 bg-card border-border space-y-4">
        <div className="flex items-start gap-3">
          <div className="p-2 rounded-lg bg-accent/10">
            <Lightbulb className="h-5 w-5 text-accent" />
          </div>
          <div className="flex-1 space-y-2">
            <h3 className="font-semibold text-lg text-foreground">Suggested Fix</h3>
            <p className="text-muted-foreground leading-relaxed whitespace-pre-wrap">
              {result.suggestion}
            </p>
          </div>
        </div>
      </Card>

      {/* Confidence Score */}
      <Card className="p-6 bg-card border-border space-y-4">
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="font-semibold text-foreground">Confidence Score</h3>
            <span className={`text-2xl font-bold ${getScoreColor(result.score)}`}>
              {result.score}/100
            </span>
          </div>
          <Progress value={result.score} className="h-2" />
          <p className="text-sm text-muted-foreground">{getScoreLabel(result.score)}</p>
        </div>

        {/* Additional Metadata Badges */}
        {(result.severity || result.bug_type) && (
          <div className="flex flex-wrap gap-2 pt-2 border-t border-border">
            {result.severity && (
              <div className="flex items-center gap-2">
                <AlertTriangle className="h-4 w-4 text-muted-foreground" />
                <Badge variant={getSeverityVariant(result.severity)}>
                  {result.severity.toUpperCase()} Severity
                </Badge>
              </div>
            )}
            {result.bug_type && (
              <div className="flex items-center gap-2">
                <Bug className="h-4 w-4 text-muted-foreground" />
                <Badge variant="outline">{result.bug_type}</Badge>
              </div>
            )}
          </div>
        )}
      </Card>

      {/* Technical Metadata */}
      <MetadataSection meta={result.meta} />
    </div>
  );
};
