// "use client";

// import React from "react";
// import { useRouter } from "next/navigation";

// const PricingComponent: React.FC = () => {
//   const router = useRouter();

//   const handleFreeClick = () => {
//     router.push("/register");
//   };

//   const handleProClick = () => {
//     alert("Payment feature coming soon 💳🚀");
//   };

//   return (
//     <section className="w-full flex flex-col items-center justify-center bg-black py-16 px-4 lg:px-8">
//       <h2 className="text-white text-5xl lg:text-6xl font-bold mb-8 leading-tight text-center">
//         Pricing
//       </h2>

//       <p className="text-gray-300 text-xl lg:text-2xl leading-relaxed mb-12 text-center max-w-4xl">
//         Start free and upgrade when you’re ready to unlock advanced AI tutoring
//         features and analytics.
//       </p>

//       <div className="w-full max-w-6xl flex flex-col md:flex-row gap-6 justify-center">
//         {/* Free Tier */}
//         <div className="bg-white rounded-3xl p-8 shadow-2xl flex-1 max-w-sm flex flex-col transform transition-all duration-300">
//           <div className="mb-4">
//             <h3 className="text-black font-semibold text-xl mb-2">Free Tier</h3>
//             <div className="flex items-end mb-2">
//               <span className="text-black text-4xl font-extrabold mr-2">
//                 ₹0
//               </span>
//               <span className="text-gray-500 text-sm mb-1">/month</span>
//             </div>
//             <p className="text-gray-700 mb-4">
//               Perfect for students exploring personalized learning.
//             </p>
//           </div>

//           <hr className="my-4 border-gray-200" />

//           <ul className="space-y-3 mb-8 text-black text-base flex-grow">
//             <li>✔ AI-generated lessons</li>
//             <li>✔ 10 topic requests/month</li>
//             <li>✔ Visual explanations</li>
//             <li>✔ Progress tracking</li>
//             <li>✔ No credit card required</li>
//           </ul>

//           <button
//             onClick={handleFreeClick}
//             className="w-full cursor-pointer bg-gray-200 text-gray-700 rounded-xl py-4 font-semibold hover:bg-gray-300 transition-all duration-300 shadow-lg hover:shadow-xl"
//           >
//             Get Started Free
//           </button>
//         </div>

//         {/* Pro Tier */}
//         <div className="bg-white rounded-3xl p-8 shadow-2xl flex-1 max-w-sm flex flex-col transform transition-all duration-300 relative">
//           <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
//             <span className="bg-black text-white px-6 py-2 rounded-full text-sm font-semibold shadow-lg">
//               Coming Soon
//             </span>
//           </div>

//           <div className="mb-4 mt-4">
//             <h3 className="text-black font-semibold text-xl mb-2">Pro Plan</h3>
//             <div className="flex items-end mb-2">
//               <span className="text-black text-4xl font-extrabold mr-2">
//                 ₹499
//               </span>
//               <span className="text-gray-500 text-sm mb-1">/month</span>
//             </div>
//             <p className="text-gray-700 mb-4">
//               For learners and educators who want advanced personalization.
//             </p>
//           </div>

//           <hr className="my-4 border-gray-200" />

//           <ul className="space-y-3 mb-8 text-black text-base flex-grow">
//             <li>✔ Unlimited topic requests</li>
//             <li>✔ AI-powered chatbot</li>
//             <li>✔ Premium support</li>
//             <li>✔ Cancel anytime</li>
//             <li>✔ Advanced analytics</li>
//           </ul>

//           <button
//             onClick={handleProClick}
//             className="w-full cursor-pointer bg-black text-white rounded-xl py-4 font-semibold hover:bg-gray-800 transition-all duration-300 shadow-lg hover:shadow-xl"
//           >
//             Upgrade to Pro
//           </button>
//         </div>
//       </div>
//     </section>
//   );
// };

// export default PricingComponent;


"use client";

import * as React from "react";
import Link from "next/link";
import { CircleCheck } from "lucide-react";

// ✅ using your existing shadcn components
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

// ---- minimal inline utility helpers ----
import clsx, { type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
const cn = (...inputs: ClassValue[]) => twMerge(clsx(inputs));

type SectionProps = { children: React.ReactNode; className?: string; id?: string };
type ContainerProps = { children: React.ReactNode; className?: string; id?: string };

const Section = ({ children, className, id }: SectionProps) => (
  <section className={cn("py-8 md:py-12", className)} id={id}>
    {children}
  </section>
);

const Container = ({ children, className, id }: ContainerProps) => (
  <div className={cn("mx-auto max-w-5xl p-6 sm:p-8", className)} id={id}>
    {children}
  </div>
);

type PlanTier = "Basic" | "Standard" | "Pro";

interface PricingCardProps {
  title: PlanTier;
  price: string;
  description?: string;
  features: string[];
  cta: string;
  href: string;
  featured?: boolean;
}

// 💰 Dummy pricing data (you can customize freely)
const pricingData: PricingCardProps[] = [
  {
    title: "Basic",
    price: "₹0 /month",
    description: "Perfect for students exploring AI tutoring.",
    features: ["3 topics/month", "Basic analytics", "Email support", "Responsive design"],
    cta: "Start Free",
    href: "/register",
  },
  {
    title: "Standard",
    price: "₹299 /month",
    description: "Best for learners who want more interactivity.",
    features: ["Unlimited topics", "Progress tracking", "24/7 support", "AI Chat Tutor"],
    cta: "Choose Standard",
    href: "/register",
    featured: true,
  },
  {
    title: "Pro",
    price: "₹499 /month",
    description: "Ideal for educators and advanced learners.",
    features: ["Full analytics", "Priority support", "AI-based feedback", "Early beta access"],
    cta: "Upgrade Now",
    href: "/register",
  },
];

export default function Pricing() {
  return (
    <Section>
      <Container className="flex flex-col items-center gap-4 text-center">
        <h2 className="!my-0 text-4xl font-bold text-white">Pricing</h2>
        <p className="text-lg text-gray-400 md:text-2xl">
          Choose the plan that fits your learning goals.
        </p>

        <div className="not-prose mt-6 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {pricingData.map((plan) => (
            <PricingCard key={plan.title} plan={plan} />
          ))}
        </div>
      </Container>
    </Section>
  );
}

function PricingCard({ plan }: { plan: PricingCardProps }) {
  return (
    <div
      className={cn(
        "flex flex-col rounded-2xl border border-gray-700 bg-black/60 backdrop-blur-md p-6 text-left transition-all duration-300 hover:border-primary hover:shadow-md",
        plan.featured && "border-primary shadow-lg ring-1 ring-primary/30 scale-[1.02]"
      )}
      aria-label={`${plan.title} plan`}
    >
      <div className="text-center">
        <div className="inline-flex items-center gap-2">
          <Badge variant={plan.featured ? "default" : "secondary"}>{plan.title}</Badge>
          {plan.featured && (
            <span className="rounded-full bg-primary/10 px-2 py-0.5 text-xs font-medium text-primary">
              Most popular
            </span>
          )}
        </div>
        <h4 className="mb-2 mt-4 text-2xl text-primary font-semibold">{plan.price}</h4>
        {plan.description && <p className="text-sm text-gray-400">{plan.description}</p>}
      </div>

      <div className="my-4 border-t border-gray-800" />

      <ul className="space-y-3">
        {plan.features.map((feature) => (
          <li key={feature} className="flex items-center text-sm text-gray-300">
            <CircleCheck className="mr-2 h-4 w-4 text-primary" />
            <span>{feature}</span>
          </li>
        ))}
      </ul>

      <div className="mt-auto pt-6">
        <Link href={plan.href}>
          <Button
            size="sm"
            className="w-full"
            variant={plan.featured ? "default" : "secondary"}
          >
            {plan.cta}
          </Button>
        </Link>
      </div>
    </div>
  );
}
