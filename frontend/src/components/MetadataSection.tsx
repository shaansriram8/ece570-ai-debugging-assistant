import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ChevronDown, ChevronUp, Cpu, Clock, Database, Wrench } from "lucide-react";
import { Button } from "@/components/ui/button";

interface MetadataSectionProps {
  meta: {
    models_used: string[];
    per_model_latency_ms: Record<string, number>;
    total_latency_ms: number;
    had_repair: boolean;
    from_cache: boolean;
    backend_version?: string;
  };
}

export const MetadataSection = ({ meta }: MetadataSectionProps) => {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <Card className="overflow-hidden bg-card border-border">
      <Button
        variant="ghost"
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full p-4 flex items-center justify-between hover:bg-muted/50 rounded-none"
      >
        <div className="flex items-center gap-2">
          <Wrench className="h-4 w-4 text-muted-foreground" />
          <span className="font-medium text-foreground">Technical Details</span>
        </div>
        {isExpanded ? (
          <ChevronUp className="h-4 w-4 text-muted-foreground" />
        ) : (
          <ChevronDown className="h-4 w-4 text-muted-foreground" />
        )}
      </Button>

      {isExpanded && (
        <div className="p-4 pt-0 space-y-4 border-t border-border animate-in slide-in-from-top-2 duration-300">
          {/* Models Used */}
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-sm font-medium text-foreground">
              <Cpu className="h-4 w-4" />
              <span>AI Models Used</span>
            </div>
            <div className="flex flex-wrap gap-2">
              {meta.models_used.map((model) => (
                <Badge key={model} variant="secondary" className="font-mono text-xs">
                  {model}
                </Badge>
              ))}
            </div>
          </div>

          {/* Latency Information */}
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-sm font-medium text-foreground">
              <Clock className="h-4 w-4" />
              <span>Response Time</span>
            </div>
            <div className="space-y-1">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Total Duration:</span>
                <span className="font-mono text-foreground">
                  {(meta.total_latency_ms / 1000).toFixed(2)}s
                </span>
              </div>
              {Object.entries(meta.per_model_latency_ms).map(([model, latency]) => (
                <div key={model} className="flex justify-between text-xs pl-4">
                  <span className="text-muted-foreground truncate max-w-[200px]">
                    {model}:
                  </span>
                  <span className="font-mono text-muted-foreground">
                    {(latency / 1000).toFixed(2)}s
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Cache and Repair Status */}
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-sm font-medium text-foreground">
              <Database className="h-4 w-4" />
              <span>Processing Details</span>
            </div>
            <div className="space-y-1 text-sm">
              <div className="flex justify-between">
                <span className="text-muted-foreground">Cache Status:</span>
                <Badge variant={meta.from_cache ? "secondary" : "outline"} className="text-xs">
                  {meta.from_cache ? "Cached" : "Fresh"}
                </Badge>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">JSON Repair:</span>
                <Badge variant={meta.had_repair ? "default" : "outline"} className="text-xs">
                  {meta.had_repair ? "Applied" : "Not Needed"}
                </Badge>
              </div>
              {meta.backend_version && (
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Backend Version:</span>
                  <span className="font-mono text-xs text-foreground">
                    {meta.backend_version}
                  </span>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </Card>
  );
};
