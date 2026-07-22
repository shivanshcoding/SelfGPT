"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { motion } from "framer-motion";
import { useForm } from "react-hook-form";
import { authApi } from "@/lib/api";
import useAuthStore from "@/stores/authStore";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Spinner } from "@/components/common/Spinner";
import { toast } from "sonner";

export default function LoginPage() {
  const router = useRouter();
  const setAuth = useAuthStore((s) => s.setAuth);
  const [isLoading, setIsLoading] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const onSubmit = async (data) => {
    setIsLoading(true);
    try {
      const response = await authApi.login(data);
      const tokens = response.data;

      // Fetch user profile
      const userRes = await authApi.me();
      
      setAuth(userRes.data, tokens.access_token, tokens.refresh_token);
      toast.success("Welcome back!");
      router.push("/chat");
    } catch (err) {
      toast.error(
        err.response?.data?.detail || "Invalid credentials. Please try again."
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="space-y-6"
    >
      <div className="space-y-2 text-center md:text-left">
        <h1 className="text-display tracking-tight text-[var(--color-text)]">
          Welcome back
        </h1>
        <p className="text-body text-[var(--color-text-secondary)]">
          Enter your credentials to continue to SelfGPT
        </p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="email">Email address</Label>
          <Input
            id="email"
            type="email"
            placeholder="name@example.com"
            {...register("email", { required: "Email is required" })}
            className={errors.email ? "border-[var(--color-error)]" : ""}
          />
          {errors.email && (
            <p className="text-sm text-[var(--color-error)]">
              {errors.email.message}
            </p>
          )}
        </div>

        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <Label htmlFor="password">Password</Label>
            <Link
              href="/forgot-password"
              className="text-sm font-medium text-[var(--color-accent)] hover:underline"
            >
              Forgot password?
            </Link>
          </div>
          <Input
            id="password"
            type="password"
            {...register("password", { required: "Password is required" })}
            className={errors.password ? "border-[var(--color-error)]" : ""}
          />
          {errors.password && (
            <p className="text-sm text-[var(--color-error)]">
              {errors.password.message}
            </p>
          )}
        </div>

        <Button
          type="submit"
          className="w-full h-11 text-base font-medium transition-all"
          style={{
            backgroundColor: "var(--color-accent)",
            color: "#fff",
            boxShadow: "var(--shadow-sm)",
          }}
          disabled={isLoading}
        >
          {isLoading ? <Spinner size="sm" color="#fff" className="mr-2" /> : null}
          {isLoading ? "Signing in..." : "Sign In"}
        </Button>
      </form>

      <div className="text-center text-sm">
        <span className="text-[var(--color-text-secondary)]">
          Don't have an account?{" "}
        </span>
        <Link
          href="/register"
          className="font-medium text-[var(--color-accent)] hover:underline"
        >
          Sign up
        </Link>
      </div>
    </motion.div>
  );
}
