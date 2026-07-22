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

export default function RegisterPage() {
  const router = useRouter();
  const setAuth = useAuthStore((s) => s.setAuth);
  const [isLoading, setIsLoading] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
  } = useForm();

  const password = watch("password");

  const onSubmit = async (data) => {
    setIsLoading(true);
    try {
      // API expects email, username, password
      const response = await authApi.register({
        email: data.email,
        username: data.username,
        password: data.password,
      });
      const tokens = response.data;

      // Fetch user profile
      const userRes = await authApi.me();
      
      setAuth(userRes.data, tokens.access_token, tokens.refresh_token);
      toast.success("Account created successfully!");
      router.push("/chat");
    } catch (err) {
      toast.error(
        err.response?.data?.detail || "Registration failed. Please try again."
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
          Create an account
        </h1>
        <p className="text-body text-[var(--color-text-secondary)]">
          Join SelfGPT and start exploring new perspectives
        </p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="username">Username</Label>
          <Input
            id="username"
            type="text"
            placeholder="johndoe"
            {...register("username", {
              required: "Username is required",
              minLength: { value: 3, message: "Minimum 3 characters" },
              maxLength: { value: 30, message: "Maximum 30 characters" },
            })}
            className={errors.username ? "border-[var(--color-error)]" : ""}
          />
          {errors.username && (
            <p className="text-sm text-[var(--color-error)]">
              {errors.username.message}
            </p>
          )}
        </div>

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
          <Label htmlFor="password">Password</Label>
          <Input
            id="password"
            type="password"
            {...register("password", {
              required: "Password is required",
              minLength: { value: 8, message: "Minimum 8 characters" },
            })}
            className={errors.password ? "border-[var(--color-error)]" : ""}
          />
          {errors.password && (
            <p className="text-sm text-[var(--color-error)]">
              {errors.password.message}
            </p>
          )}
        </div>

        <div className="space-y-2">
          <Label htmlFor="confirmPassword">Confirm Password</Label>
          <Input
            id="confirmPassword"
            type="password"
            {...register("confirmPassword", {
              required: "Please confirm your password",
              validate: (value) =>
                value === password || "Passwords do not match",
            })}
            className={errors.confirmPassword ? "border-[var(--color-error)]" : ""}
          />
          {errors.confirmPassword && (
            <p className="text-sm text-[var(--color-error)]">
              {errors.confirmPassword.message}
            </p>
          )}
        </div>

        <Button
          type="submit"
          className="w-full h-11 text-base font-medium transition-all mt-2"
          style={{
            backgroundColor: "var(--color-accent)",
            color: "#fff",
            boxShadow: "var(--shadow-sm)",
          }}
          disabled={isLoading}
        >
          {isLoading ? <Spinner size="sm" color="#fff" className="mr-2" /> : null}
          {isLoading ? "Creating account..." : "Sign Up"}
        </Button>
      </form>

      <div className="text-center text-sm">
        <span className="text-[var(--color-text-secondary)]">
          Already have an account?{" "}
        </span>
        <Link
          href="/login"
          className="font-medium text-[var(--color-accent)] hover:underline"
        >
          Sign in
        </Link>
      </div>
    </motion.div>
  );
}
