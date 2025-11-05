'use client';

import { useState, useEffect } from 'react';
// OLD: import Sidebar from '@/app/components/Sidebar';
import { AppLayout } from '@/components/app-layout';
import { Lock, Check, Clock, TrendingUp, Target, Award, Sparkles, Trophy } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { cn } from '@/lib/utils';

interface Skill {
  id: number;
  name: string;
  description: string;
  category: string;
  difficulty: string;
  estimated_hours: number;
  prerequisite_ids: number[];
  is_unlocked: boolean;
  mastery_level: number;
  progress_percentage: number;
}

interface SkillNode extends Skill {
  x: number;
  y: number;
}

export default function SkillTreePage() {
  const [skills, setSkills] = useState<Skill[]>([]);
  const [selectedSkill, setSelectedSkill] = useState<Skill | null>(null);
  const [filter, setFilter] = useState<string>('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSkillTree();
  }, []);

  const fetchSkillTree = async () => {
    try {
      const token = localStorage.getItem('token');
      const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8002';
      const response = await fetch(`${API_BASE}/api/v1/mastery/skills/tree`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        const data = await response.json();
        setSkills(data.tree.nodes);
      }
    } catch (error) {
      console.error('Error fetching skill tree:', error);
    } finally {
      setLoading(false);
    }
  };

  const getMasteryColor = (level: number) => {
    // OLD: Purple color removed from palette
    // const colors = ['#9CA3AF', '#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6'];
    const colors = ['#9CA3AF', '#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#10B981']; // Green instead of purple
    return colors[level] || colors[0];
  };

  const getMasteryLabel = (level: number) => {
    const labels = ['Not Started', 'Beginner', 'Developing', 'Proficient', 'Advanced', 'Master'];
    return labels[level] || labels[0];
  };

  const filteredSkills = skills.filter(skill => {
    if (filter === 'all') return true;
    if (filter === 'unlocked') return skill.is_unlocked;
    if (filter === 'locked') return !skill.is_unlocked;
    if (filter === 'mastered') return skill.mastery_level >= 5;
    return skill.category === filter;
  });

  const categories = [...new Set(skills.map(s => s.category))];
  const statsData = {
    total: skills.length,
    unlocked: skills.filter(s => s.is_unlocked).length,
    mastered: skills.filter(s => s.mastery_level >= 5).length,
    inProgress: skills.filter(s => s.mastery_level > 0 && s.mastery_level < 5).length
  };

  if (loading) {
    return (
      <AppLayout title="Skill Tree" showBackButton>
        <div className="flex items-center justify-center h-[calc(100vh-12rem)]">
          <div className="text-center">
            <Sparkles className="w-12 h-12 text-primary animate-pulse mx-auto mb-4" />
            <p className="text-lg text-muted-foreground">Loading Skill Tree...</p>
          </div>
        </div>
      </AppLayout>
    );
  }

  return (
    <AppLayout title="Skill Tree" showBackButton>
      <div className="container mx-auto max-w-7xl p-6">
        {/* Header Card */}
        <Card className="mb-6">
          <CardHeader>
            <div className="flex items-center gap-3">
              <div className="p-2 bg-accent/10 rounded-lg">
                <Trophy className="w-6 h-6 text-accent" />
              </div>
              <div>
                <CardTitle>Skill Tree</CardTitle>
                <CardDescription>Master skills to unlock new learning paths</CardDescription>
              </div>
            </div>
          </CardHeader>
        </Card>

        {/* Stats - OLD: Purple color removed */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-muted-foreground">Total Skills</p>
                    <p className="text-3xl font-bold">{statsData.total}</p>
                  </div>
                  <Target className="w-8 h-8 text-primary" />
                </div>
              </CardContent>
            </Card>
          </motion.div>
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-muted-foreground">Unlocked</p>
                    <p className="text-3xl font-bold text-accent">{statsData.unlocked}</p>
                  </div>
                  <Check className="w-8 h-8 text-accent" />
                </div>
              </CardContent>
            </Card>
          </motion.div>
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}>
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-muted-foreground">In Progress</p>
                    <p className="text-3xl font-bold text-orange-600 dark:text-orange-400">{statsData.inProgress}</p>
                  </div>
                  <TrendingUp className="w-8 h-8 text-orange-600 dark:text-orange-400" />
                </div>
              </CardContent>
            </Card>
          </motion.div>
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }}>
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-muted-foreground">Mastered</p>
                    {/* OLD: text-purple-600 changed to text-accent */}
                    <p className="text-3xl font-bold text-accent">{statsData.mastered}</p>
                  </div>
                  {/* OLD: text-purple-500 changed to text-accent */}
                  <Award className="w-8 h-8 text-accent" />
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>

        {/* Filters - OLD: Purple button changed to accent */}
        <Card className="mb-6">
          <CardContent className="p-4">
            <div className="flex flex-wrap gap-2">
              <Button
                variant={filter === 'all' ? 'default' : 'secondary'}
                size="sm"
                onClick={() => setFilter('all')}
              >
                All Skills
              </Button>
              <Button
                variant={filter === 'unlocked' ? 'default' : 'secondary'}
                size="sm"
                onClick={() => setFilter('unlocked')}
                className={filter === 'unlocked' ? 'bg-accent hover:bg-accent/90' : ''}
              >
                Unlocked
              </Button>
              <Button
                variant={filter === 'locked' ? 'default' : 'secondary'}
                size="sm"
                onClick={() => setFilter('locked')}
              >
                Locked
              </Button>
              {/* OLD: bg-purple-600 changed to bg-accent */}
              <Button
                variant={filter === 'mastered' ? 'default' : 'secondary'}
                size="sm"
                onClick={() => setFilter('mastered')}
                className={filter === 'mastered' ? 'bg-accent hover:bg-accent/90' : ''}
              >
                Mastered
              </Button>
              {categories.map(cat => (
                <Button
                  key={cat}
                  variant={filter === cat ? 'default' : 'secondary'}
                  size="sm"
                  onClick={() => setFilter(cat)}
                >
                  {cat}
                </Button>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Skills Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <AnimatePresence>
            {filteredSkills.map((skill, index) => (
              <motion.div
                key={skill.id}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.05 }}
              >
                <Card
                  className={cn(
                    "cursor-pointer hover:shadow-lg transition-all",
                    !skill.is_unlocked && "opacity-60"
                  )}
                  style={{ borderLeft: `4px solid ${getMasteryColor(skill.mastery_level)}` }}
                  onClick={() => setSelectedSkill(skill)}
                >
                  <CardContent className="p-4">
                    <div className="flex items-start justify-between mb-2">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          {!skill.is_unlocked && <Lock className="w-4 h-4 text-muted-foreground" />}
                          {/* OLD: text-purple-600 changed to text-accent */}
                          {skill.mastery_level >= 5 && <Award className="w-4 h-4 text-accent" />}
                          <h3 className="font-semibold">{skill.name}</h3>
                        </div>
                        <p className="text-xs text-muted-foreground">{skill.category}</p>
                      </div>
                      <span className={cn(
                        "px-2 py-1 text-xs rounded-full",
                        skill.difficulty === 'beginner' && 'bg-accent/20 text-accent',
                        skill.difficulty === 'intermediate' && 'bg-primary/20 text-primary',
                        skill.difficulty === 'advanced' && 'bg-orange-500/20 text-orange-600 dark:text-orange-400',
                        skill.difficulty === 'expert' && 'bg-destructive/20 text-destructive'
                      )}>
                        {skill.difficulty}
                      </span>
                    </div>

                    <p className="text-sm text-muted-foreground mb-3 line-clamp-2">{skill.description}</p>

                    {/* Progress Bar */}
                    <div className="mb-2">
                      <div className="flex justify-between text-xs mb-1">
                        <span className="text-muted-foreground">{getMasteryLabel(skill.mastery_level)}</span>
                        <span className="text-muted-foreground">{Math.round(skill.progress_percentage)}%</span>
                      </div>
                      <div className="w-full bg-muted rounded-full h-2">
                        <motion.div
                          initial={{ width: 0 }}
                          animate={{ width: `${skill.progress_percentage}%` }}
                          transition={{ duration: 1, delay: index * 0.05 + 0.3 }}
                          className="h-2 rounded-full"
                          style={{ backgroundColor: getMasteryColor(skill.mastery_level) }}
                        />
                      </div>
                    </div>

                    <div className="flex items-center gap-2 text-xs text-muted-foreground">
                      <Clock className="w-3 h-3" />
                      <span>{skill.estimated_hours}h to master</span>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </AnimatePresence>
        </div>

        {filteredSkills.length === 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-12"
          >
            <Card>
              <CardContent className="p-12">
                <Target className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
                <p className="text-muted-foreground">No skills found matching your filter</p>
              </CardContent>
            </Card>
          </motion.div>
        )}

        {/* Skill Detail Modal */}
        <AnimatePresence>
          {selectedSkill && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50"
              onClick={() => setSelectedSkill(null)}
            >
              <motion.div
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.9, opacity: 0 }}
                onClick={e => e.stopPropagation()}
              >
                <Card className="max-w-2xl w-full max-h-[90vh] overflow-y-auto">
                  <CardHeader>
                    <CardTitle className="text-2xl">{selectedSkill.name}</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div>
                      <p className="text-sm text-muted-foreground mb-1">Category</p>
                      <p className="font-semibold">{selectedSkill.category}</p>
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground mb-1">Description</p>
                      <p>{selectedSkill.description}</p>
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground mb-1">Mastery Level</p>
                      <div className="flex items-center gap-3">
                        <div className="flex-1">
                          <div className="w-full bg-muted rounded-full h-3">
                            <motion.div
                              initial={{ width: 0 }}
                              animate={{ width: `${selectedSkill.progress_percentage}%` }}
                              transition={{ duration: 1 }}
                              className="h-3 rounded-full"
                              style={{ backgroundColor: getMasteryColor(selectedSkill.mastery_level) }}
                            />
                          </div>
                        </div>
                        <span className="font-semibold">{getMasteryLabel(selectedSkill.mastery_level)}</span>
                      </div>
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <p className="text-sm text-muted-foreground mb-1">Difficulty</p>
                        <p className="font-semibold capitalize">{selectedSkill.difficulty}</p>
                      </div>
                      <div>
                        <p className="text-sm text-muted-foreground mb-1">Estimated Time</p>
                        <p className="font-semibold">{selectedSkill.estimated_hours} hours</p>
                      </div>
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground mb-1">Status</p>
                      <p className="font-semibold flex items-center gap-2">
                        {selectedSkill.is_unlocked ? (
                          <><Check className="w-4 h-4 text-accent" /> Unlocked</>
                        ) : (
                          <><Lock className="w-4 h-4 text-muted-foreground" /> Locked - Complete prerequisites first</>
                        )}
                      </p>
                    </div>
                    <div className="flex gap-2 pt-4">
                      {selectedSkill.is_unlocked && selectedSkill.mastery_level < 5 && (
                        <Button className="flex-1">
                          Start Learning
                        </Button>
                      )}
                      <Button
                        variant="outline"
                        onClick={() => setSelectedSkill(null)}
                      >
                        Close
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </AppLayout>
  );
}
