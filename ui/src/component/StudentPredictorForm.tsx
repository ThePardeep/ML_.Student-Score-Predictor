import React, { Dispatch, SetStateAction, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Button } from "@/components/ui/button";

interface StudentData {
  gender: string;
  race_ethnicity: string;
  parental_level_of_education: string;
  lunch: string;
  test_preparation_course: string;
  reading_score: number;
  writing_score: number;
}
interface StudentPredictorFormProps {
  setPredictedScore: Dispatch<SetStateAction<number | null>>;
}
const StudentPredictorForm: React.FC<StudentPredictorFormProps> = ({
  setPredictedScore,
}) => {
  const [formData, setFormData] = useState<StudentData>({
    gender: "",
    race_ethnicity: "",
    parental_level_of_education: "",
    lunch: "",
    test_preparation_course: "",
    reading_score: 0,
    writing_score: 0,
  });

  const handleChange = (field: keyof StudentData, value: string | number) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handlePredict = async () => {
    try {
      const response = await fetch("http://localhost:4000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const result = await response.json();
      if (result.predicted_score !== undefined) {
        setPredictedScore(result.predicted_score || 0);
      } else {
        setPredictedScore(0);
        alert("Please select valid input data.");
      }
    } catch (error) {
      setPredictedScore(0);
      console.error("Prediction error:", error);
      alert("Server error or ");
    }
  };

  return (
    <div className="mx-auto">
      <Card className="p-6 shadow-xl rounded-2xl">
        <CardContent className="space-y-4">
          <h2 className="text-2xl font-semibold">
            Student Performance Predictor
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label className="mb-2">Gender</Label>
              <Select onValueChange={(value) => handleChange("gender", value)}>
                <SelectTrigger>
                  <SelectValue placeholder="Select gender" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="male">Male</SelectItem>
                  <SelectItem value="female">Female</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label className="mb-2">Race/Ethnicity</Label>
              <Select
                onValueChange={(value) => handleChange("race_ethnicity", value)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select group" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="group A">Group A</SelectItem>
                  <SelectItem value="group B">Group B</SelectItem>
                  <SelectItem value="group C">Group C</SelectItem>
                  <SelectItem value="group D">Group D</SelectItem>
                  <SelectItem value="group E">Group E</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label className="mb-2">Parental Level of Education</Label>
              <Select
                onValueChange={(value) =>
                  handleChange("parental_level_of_education", value)
                }
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select education level" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="high school">High School</SelectItem>
                  <SelectItem value="some high school">
                    Some High School
                  </SelectItem>
                  <SelectItem value="associate's degree">
                    Associate&apos;s Degree
                  </SelectItem>
                  <SelectItem value="some college">Some College</SelectItem>
                  <SelectItem value="bachelor's degree">
                    Bachelor&apos;s Degree
                  </SelectItem>
                  <SelectItem value="master's degree">
                    Master&apos;s Degree
                  </SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label className="mb-2">Lunch</Label>
              <Select onValueChange={(value) => handleChange("lunch", value)}>
                <SelectTrigger>
                  <SelectValue placeholder="Select lunch type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="standard">Standard</SelectItem>
                  <SelectItem value="free/reduced">Free/Reduced</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label className="mb-2">Reading Score</Label>
              <Input
                type="number"
                placeholder="Enter reading score"
                min={0}
                max={100}
                value={formData.reading_score}
                onChange={(e) =>
                  handleChange("reading_score", Number(e.target.value))
                }
              />
            </div>

            <div>
              <Label className="mb-2">Writing Score</Label>
              <Input
                type="number"
                placeholder="Enter writing score"
                min={0}
                max={100}
                value={formData.writing_score}
                onChange={(e) =>
                  handleChange("writing_score", Number(e.target.value))
                }
              />
            </div>
          </div>

          <div>
              <Label className="mb-2">Test Preparation Course</Label>
              <Select
                onValueChange={(value) =>
                  handleChange("test_preparation_course", value)
                }
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select course status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="none">None</SelectItem>
                  <SelectItem value="completed">Completed</SelectItem>
                </SelectContent>
              </Select>
            </div>


          <Button className="w-full mt-4" onClick={handlePredict}>
            Predict
          </Button>
        </CardContent>
      </Card>
    </div>
  );
};

export default StudentPredictorForm;
