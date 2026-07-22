"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { useForm } from "react-hook-form";
import { api } from "@/lib/api";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Spinner } from "@/components/common/Spinner";
import { ArrowLeft } from "lucide-react";
import Link from "next/link";

export default function CreateIdentityPage() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  
  const { register, handleSubmit, formState: { errors } } = useForm({
    defaultValues: {
      name: "",
      tone: "professional and helpful",
      knowledge_domain: "general knowledge",
      traits: "curious, friendly, concise"
    }
  });

  const onSubmit = async (data) => {
    setIsLoading(true);
    try {
      const payload = {
        name: data.name,
        profile: {
          name: data.name,
          tone: data.tone,
          knowledge_domain: data.knowledge_domain,
          traits: data.traits.split(",").map(t => t.trim()),
          rules: ["Never break character", "Be helpful"]
        }
      };
      
      const res = await api.post("/api/identities/custom", payload);
      toast.success("Custom identity created successfully!");
      
      // Start a chat with the new custom identity
      const chatRes = await api.post("/api/chats/", {
        identity_id: res.data.slug,
        title: `Chat with ${res.data.name}`
      });
      
      router.push(`/chat/${chatRes.data.id}`);
    } catch (err) {
      toast.error(err.response?.data?.detail || "Failed to create identity.");
      setIsLoading(false);
    }
  };

  return (
    <div className="flex-1 overflow-y-auto bg-[var(--color-bg)] p-6 md:p-12">
      <div className="max-w-2xl mx-auto space-y-8">
        <Link 
          href="/chat" 
          className="inline-flex items-center text-sm font-medium text-[var(--color-text-secondary)] hover:text-[var(--color-text)] transition-colors"
        >
          <ArrowLeft size={16} className="mr-2" />
          Back to Identities
        </Link>
        
        <div>
          <h1 className="text-display font-semibold text-[var(--color-text)]">
            Create Custom AI
          </h1>
          <p className="text-body text-[var(--color-text-secondary)] mt-2">
            Design an AI tailored to your exact needs. We'll automatically generate the perfect system prompt for you.
          </p>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="name">AI Name</Label>
            <Input 
              id="name" 
              placeholder="e.g. Code Reviewer Pro, or Study Buddy" 
              {...register("name", { required: "Name is required" })}
              className={errors.name ? "border-[var(--color-error)]" : ""}
            />
            {errors.name && <p className="text-sm text-[var(--color-error)]">{errors.name.message}</p>}
          </div>

          <div className="space-y-2">
            <Label htmlFor="knowledge_domain">Knowledge Domain & Expertise</Label>
            <Input 
              id="knowledge_domain" 
              placeholder="e.g. Frontend web development, React, and UX design" 
              {...register("knowledge_domain")}
            />
            <p className="text-xs text-[var(--color-text-muted)]">What should this AI be an expert in?</p>
          </div>

          <div className="space-y-2">
            <Label htmlFor="tone">Tone of Voice</Label>
            <Input 
              id="tone" 
              placeholder="e.g. Sarcastic, formal, enthusiastic" 
              {...register("tone")}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="traits">Key Traits (Comma separated)</Label>
            <Input 
              id="traits" 
              placeholder="e.g. analytical, concise, direct" 
              {...register("traits")}
            />
          </div>

          <Button 
            type="submit" 
            disabled={isLoading}
            className="w-full"
            style={{ backgroundColor: "var(--color-accent)", color: "#fff" }}
          >
            {isLoading ? <Spinner size="sm" color="#fff" className="mr-2" /> : null}
            {isLoading ? "Creating..." : "Create Identity & Start Chat"}
          </Button>
        </form>
      </div>
    </div>
  );
}
