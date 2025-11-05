'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/app/contexts/AuthContext';
import { AppLayout } from '@/components/app-layout';
import { Target, TrendingUp, Clock, AlertTriangle, CheckCircle, RefreshCw, Sparkles, Award } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { cn } from '@/lib/utils';

interface SkillGap {
    id: number;
    skill_name: string;
    current_level: number;
    target_level: number;
    severity: string;
    priority: number;
    estimated_time_hours: number;
    recommendations: string[];
    progress: number;
    created_at: string;
}

export default function SkillGapsPage() {
    const router = useRouter();
    const { isAuthenticated, user } = useAuth();
    const [gaps, setGaps] = useState<SkillGap[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (!isAuthenticated) {
            router.push('/login');
            return;
        }
        loadGaps();
    }, [isAuthenticated]);

    const loadGaps = async () => {
        try {
            setIsLoading(true);
            const token = localStorage.getItem('token');
            if (!token) {
                throw new Error('Please log in to view skill gaps');
            }

            const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8002';
            const response = await fetch(`${API_BASE}/api/v1/skill-gaps/list`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            });

            if (!response.ok) {
                throw new Error('Failed to load skill gaps');
            }

            const data = await response.json();
            setGaps(data);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    const analyzeGaps = async () => {
        try {
            setIsAnalyzing(true);
            const token = localStorage.getItem('token');
            if (!token) {
                throw new Error('Please log in to analyze gaps');
            }

            const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8002';
            const response = await fetch(`${API_BASE}/api/v1/skill-gaps/analyze`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            });

            if (!response.ok) {
                throw new Error('Failed to analyze gaps');
            }

            await loadGaps();
        } catch (err: any) {
            setError(err.message);
        } finally {
            setIsAnalyzing(false);
        }
    };

    const getSeverityColor = (severity: string) => {
        switch (severity.toLowerCase()) {
            case 'critical': return 'text-destructive bg-destructive/10 border-destructive/30';
            case 'high': return 'text-orange-600 dark:text-orange-400 bg-orange-500/10 border-orange-500/30';
            case 'medium': return 'text-yellow-600 dark:text-yellow-400 bg-yellow-500/10 border-yellow-500/30';
            case 'low': return 'text-accent bg-accent/10 border-accent/30';
            default: return 'text-muted-foreground bg-muted border-border';
        }
    };

    const getSeverityIcon = (severity: string) => {
        switch (severity.toLowerCase()) {
            case 'critical':
            case 'high':
                return <AlertTriangle className="w-5 h-5" />;
            case 'medium':
                return <Target className="w-5 h-5" />;
            case 'low':
                return <CheckCircle className="w-5 h-5" />;
            default:
                return <Target className="w-5 h-5" />;
        }
    };

    if (isLoading) {
        return (
            <AppLayout title="Skill Gap Analysis" showBackButton>
                <div className="flex items-center justify-center h-[calc(100vh-12rem)]">
                    <div className="text-center">
                        <RefreshCw className="w-12 h-12 text-primary animate-spin mx-auto mb-4" />
                        <p className="text-lg text-muted-foreground">Loading skill gaps...</p>
                    </div>
                </div>
            </AppLayout>
        );
    }

    return (
        <AppLayout title="Skill Gap Analysis" showBackButton>
            <div className="container mx-auto max-w-7xl p-6">
                {/* Header Card */}
                <Card className="mb-6">
                    <CardHeader>
                        <div className="flex justify-between items-start">
                            <div className="flex items-center gap-3">
                                <div className="p-2 bg-primary/10 rounded-lg">
                                    <Target className="w-6 h-6 text-primary" />
                                </div>
                                <div>
                                    <CardTitle>Skill Gap Analysis</CardTitle>
                                    <CardDescription>Identify and track your learning gaps with AI-powered insights</CardDescription>
                                </div>
                            </div>
                            <Button
                                onClick={analyzeGaps}
                                disabled={isAnalyzing}
                                className="gap-2"
                            >
                                <RefreshCw className={cn("w-4 h-4", isAnalyzing && "animate-spin")} />
                                {isAnalyzing ? 'Analyzing...' : 'Analyze Gaps'}
                            </Button>
                        </div>
                    </CardHeader>
                </Card>

                {error && (
                    <motion.div
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="mb-6"
                    >
                        <Card className="border-destructive/50 bg-destructive/10">
                            <CardContent className="p-4">
                                <p className="text-sm text-destructive">{error}</p>
                            </CardContent>
                        </Card>
                    </motion.div>
                )}

                {gaps.length === 0 ? (
                    <motion.div
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        className="text-center py-16"
                    >
                        <div className="p-4 bg-primary/10 rounded-full inline-block mb-4">
                            <Target className="w-12 h-12 text-primary" />
                        </div>
                        <h3 className="text-xl font-semibold mb-2">No skill gaps detected</h3>
                        <p className="text-muted-foreground mb-6">
                            {isAnalyzing ? 'Analyzing your performance...' : 'Click "Analyze Gaps" to identify areas for improvement'}
                        </p>
                    </motion.div>
                ) : (
                    <>
                        {/* Summary Stats */}
                        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
                                <Card>
                                    <CardContent className="p-6">
                                        <div className="flex items-center gap-3 mb-2">
                                            <Target className="w-5 h-5 text-primary" />
                                            <h3 className="text-sm text-muted-foreground">Total Gaps</h3>
                                        </div>
                                        <p className="text-3xl font-bold">{gaps.length}</p>
                                    </CardContent>
                                </Card>
                            </motion.div>

                            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
                                <Card>
                                    <CardContent className="p-6">
                                        <div className="flex items-center gap-3 mb-2">
                                            <AlertTriangle className="w-5 h-5 text-destructive" />
                                            <h3 className="text-sm text-muted-foreground">Critical</h3>
                                        </div>
                                        <p className="text-3xl font-bold text-destructive">
                                            {gaps.filter(g => g.severity.toLowerCase() === 'critical').length}
                                        </p>
                                    </CardContent>
                                </Card>
                            </motion.div>

                            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}>
                                <Card>
                                    <CardContent className="p-6">
                                        <div className="flex items-center gap-3 mb-2">
                                            <Clock className="w-5 h-5 text-primary" />
                                            <h3 className="text-sm text-muted-foreground">Est. Time</h3>
                                        </div>
                                        <p className="text-3xl font-bold">
                                            {gaps.reduce((sum, g) => sum + g.estimated_time_hours, 0)}h
                                        </p>
                                    </CardContent>
                                </Card>
                            </motion.div>

                            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }}>
                                <Card>
                                    <CardContent className="p-6">
                                        <div className="flex items-center gap-3 mb-2">
                                            <TrendingUp className="w-5 h-5 text-accent" />
                                            <h3 className="text-sm text-muted-foreground">Avg Progress</h3>
                                        </div>
                                        <p className="text-3xl font-bold text-accent">
                                            {Math.round(gaps.reduce((sum, g) => sum + g.progress, 0) / gaps.length)}%
                                        </p>
                                    </CardContent>
                                </Card>
                            </motion.div>
                        </div>

                        {/* Skill Gaps List */}
                        <div className="space-y-4">
                            <h2 className="text-2xl font-bold mb-4">Your Skill Gaps</h2>
                            <AnimatePresence>
                                {gaps.sort((a, b) => b.priority - a.priority).map((gap, index) => (
                                    <motion.div
                                        key={gap.id}
                                        initial={{ opacity: 0, y: 20 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        transition={{ delay: index * 0.1 }}
                                    >
                                        <Card className="hover:shadow-lg transition-shadow">
                                            <CardContent className="p-6">
                                                <div className="flex items-start justify-between mb-4">
                                                    <div className="flex-1">
                                                        <div className="flex items-center gap-3 mb-2 flex-wrap">
                                                            <h3 className="text-xl font-semibold">{gap.skill_name}</h3>
                                                            <span className={cn("flex items-center gap-1 px-3 py-1 rounded-full text-xs border font-medium", getSeverityColor(gap.severity))}>
                                                                {getSeverityIcon(gap.severity)}
                                                                {gap.severity}
                                                            </span>
                                                        </div>
                                                        <div className="flex items-center gap-4 text-sm text-muted-foreground">
                                                            <span>Priority: {gap.priority}/10</span>
                                                            <span>•</span>
                                                            <span className="flex items-center gap-1">
                                                                <Clock className="w-4 h-4" />
                                                                {gap.estimated_time_hours}h estimated
                                                            </span>
                                                        </div>
                                                    </div>
                                                </div>

                                                {/* Progress Bar */}
                                                <div className="mb-4">
                                                    <div className="flex justify-between text-sm mb-2">
                                                        <span className="text-muted-foreground">Current: {gap.current_level}/10</span>
                                                        <span className="text-muted-foreground">Target: {gap.target_level}/10</span>
                                                    </div>
                                                    <div className="w-full bg-muted rounded-full h-3 overflow-hidden">
                                                        <motion.div
                                                            initial={{ width: 0 }}
                                                            animate={{ width: `${gap.progress}%` }}
                                                            transition={{ duration: 1, delay: index * 0.1 + 0.3 }}
                                                            className="h-full bg-gradient-to-r from-primary to-accent"
                                                        />
                                                    </div>
                                                    <p className="text-sm text-muted-foreground mt-1">{gap.progress}% complete</p>
                                                </div>

                                                {/* Recommendations */}
                                                {gap.recommendations && gap.recommendations.length > 0 && (
                                                    <div className="bg-muted/50 rounded-lg p-4">
                                                        <h4 className="font-semibold mb-2 text-primary flex items-center gap-2">
                                                            <Award className="w-4 h-4" />
                                                            Recommendations:
                                                        </h4>
                                                        <ul className="space-y-1">
                                                            {gap.recommendations.map((rec, idx) => (
                                                                <li key={idx} className="text-sm flex items-start gap-2">
                                                                    <span className="text-primary mt-1">•</span>
                                                                    <span>{rec}</span>
                                                                </li>
                                                            ))}
                                                        </ul>
                                                    </div>
                                                )}
                                            </CardContent>
                                        </Card>
                                    </motion.div>
                                ))}
                            </AnimatePresence>
                        </div>
                    </>
                )}
            </div>
        </AppLayout>
    );
}
