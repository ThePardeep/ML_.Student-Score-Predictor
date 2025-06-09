"use client";

import StudentPredictorForm from "@/component/StudentPredictorForm";
import { Card, CardContent } from "@/components/ui/card";
import { useState } from "react";

export default function Home() {
  const [predictedScore, setPredictedScore] = useState<number | null>(null);
  return (
    <div className="flex flex-col gap-2 p-4">
      <div>
        <StudentPredictorForm setPredictedScore={setPredictedScore} />
      </div>

      <Card className="p-6 shadow-xl rounded-2xl">
        <div className="mt-6 p-4 bg-green-100 text-green-800 rounded-xl text-center text-lg">
          Predicted Math Score: <strong>{predictedScore}</strong>
        </div>
        <CardContent className="space-y-4"></CardContent>
      </Card>
    </div>
  );
}
