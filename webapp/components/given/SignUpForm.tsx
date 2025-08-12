"use client";

import { cn } from "@/lib/utils/utils";
import { Button } from "@radix-ui/themes";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/Card";
import { Input } from "@/components/ui/Input";
import { Label } from "@/components/ui/Label";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { useAuth } from "@/lib/contexts/AuthContext";
import { CreateUserParams } from "@/lib/types";

export function SignUpForm({
  className,
  ...props
}: React.ComponentPropsWithoutRef<"div">) {

  const [signUpData, setSignUpData] = useState<CreateUserParams>({
    username: "",
    email: "",
    phoneNumber: "",
    password: "",
    repeatPassword: "",
  });

  const [error, setError] = useState<string | null>(null);
  const router = useRouter();
  const { signUp, isLoading } = useAuth();

  const handleSignUp = async (e: React.FormEvent) => {
    e.preventDefault();
    await signUp(signUpData);
  };

  const handleInputChange = (field: keyof CreateUserParams) => (e: React.ChangeEvent<HTMLInputElement>) => {
    setSignUpData(prev => ({
      ...prev,
      [field]: e.target.value
    }));
  }

  return (
    <div className={cn("flex flex-col gap-6", className)} {...props}>
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl">Sign up</CardTitle>
          <CardDescription>Create a new account</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSignUp}>
            <div className="flex flex-col gap-6">
              <div className="grid gap-2">
                <Label htmlFor="username">Username</Label>
                <Input
                    id="username"
                    type="username"
                    placeholder="username"
                    required
                    value={signUpData.username}
                    onChange={handleInputChange('username')}
                />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="email">Email</Label>
                <Input
                    id="email"
                    type="email"
                    placeholder="m@example.com"
                    required
                    value={signUpData.email}
                    onChange={handleInputChange('email')}
                />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="phone">Phone</Label>
                <Input
                    id="phone"
                    type="tel"
                    placeholder="(123) 456 - 7890"
                    pattern={"[0-9]{3}-[0-9]{3}-[0-9]{4}"}
                    required
                    value={signUpData.phoneNumber}
                    onChange={handleInputChange('phoneNumber')}
                />
              </div>
              <div className="grid gap-2">
                <div className="flex items-center">
                  <Label htmlFor="password">Password</Label>
                </div>
                <Input
                    id="password"
                    type="password"
                    required
                    value={signUpData.password}
                    onChange={handleInputChange('password')}
                />
              </div>
              <div className="grid gap-2">
                <div className="flex items-center">
                  <Label htmlFor="repeat-password">Repeat Password</Label>
                </div>
                <Input
                    id="repeat-password"
                    type="password"
                    required
                    value={signUpData.repeatPassword}
                    onChange={handleInputChange('repeatPassword')}
                />
              </div>
              {error && <p className="text-sm text-red-500">{error}</p>}
              <Button type="submit" className="w-full" disabled={isLoading}>
                {isLoading ? "Creating an account..." : "Sign up"}
              </Button>
            </div>
            <div className="mt-4 text-center text-sm">
              Already have an account?{" "}
              <Link href="/login" className="underline underline-offset-4">
                Login
              </Link>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
