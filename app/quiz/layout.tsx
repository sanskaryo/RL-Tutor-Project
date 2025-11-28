import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AI Tutor Quiz | RL-Tutor",
  description: "Personalized learning session powered by Reinforcement Learning",
};

export default function QuizLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="bg-black min-h-screen">
      {children}
    </div>
  );
}
