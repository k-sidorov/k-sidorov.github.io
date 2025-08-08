---
layout: post
title: "A new approach to solving hard scheduling problems via disjointness"
description: An overview of the scheduling technique explored by us in our CP 2025 conference submission.
tags: cp scheduling
categories: paper-announcement
related_posts: false
featured: true
toc:
  sidebar: left
---

I'm excited to share that my latest paper, “Unite and Lead: Finding Disjunctive Cliques for Scheduling Problems,” co-authored with [Imko Marijnissen](https://imkomarijnissen.com) and [Emir Demirović](https://emirdemirovic.com), has been accepted to CP 2025! For those who want all the technical details, you can read the full paper [here]({{ "/assets/pdf/cp2025-unite-and-lead.pdf" | relative_url }}). But for everyone else, I wanted to write this post to explain the core ideas in a more accessible way.

## The blind spots of specialization

Imagine you're managing a very complex project—like building a factory or designing a CPU. You have hundreds of tasks, and each task requires specific resources: a certain number of workers, a particular machine, a specific tool, and so on. Your goal is to create a schedule that completes the project as quickly as possible without any resource conflicts (like needing 11 workers when you only have 10).

This is a classic **scheduling problem**. In the world of computer science, we frequently use general-purpose software tools called “solvers” to tackle them. These solvers are smart, but the constraint programming solvers—the ones commonly used in scheduling—have a particular way of looking at the problem: they focus on one constraint at a time.

A solver might look at the “workers” constraint and ensure you never schedule too many tasks at once for your team. Then, it will separately look at the “machine” constraint to make sure the machine isn't double-booked. This is a very effective strategy, but it can create blind spots. By looking at each resource in isolation, the solver can miss the bigger picture—the _global structure_ of the problem that arises from how different constraints interact.

In a way, it's like trying to solve a Sudoku puzzle by only ever looking at one row at a time, then one column at a time, and then one 3x3 box at a time. Sure, this is a plausible strategy, and with proper accounting, it eventually succeeds; however, this way you will miss crucial insights!

## A puzzle that fools modern solvers

To see how the local view can fail, consider a small puzzle; in our work, we call it the _3n problem_. Let's say you have six tasks. Each requires a different mix of three resources. Your job is to schedule them. Try it for yourself below! You can drag the tasks onto the timeline. **Can you schedule any two tasks at the same time?**

<iframe class="iframe-resize" src="{{ '/assets/html/cp2025-3n.html' | relative_url }}" frameborder='0' scrolling='no'></iframe>

As you surely discovered by this point, you can't. Any pair of tasks you choose will overload one of the resources. For example:
- Two yellow tasks conflict on Resource 1.
- A yellow and a green task conflict on Resource 1.
- A yellow and a blue task conflict on Resource 2.

…and so on.

Every single pair of tasks is **disjoint**—they cannot overlap in time. The only solution is to schedule all six tasks sequentially, one after the other. This seems obvious when you look at the whole picture. But for a standard constraint solver, it's surprisingly tricky:
- The solver checks the “Resource 1” constraint and sees _some_ pairs of tasks in conflict.
- Then it checks the “Resource 2” and finds _some other_ conflicting pairs.

But no single resource constraint tells the solver that _all_ tasks are pairwise disjoint. To figure that out, it needs to combine the information from all three resource constraints. Without a mechanism to do this, the solver resorts to brute-force trial and error, which takes exorbitant amounts of time for larger versions of this puzzle.

## Our solution: the disjointness detective

This is where our work comes in. We give the solver a new set of tools to reason about the global structure of the problem by focusing on this idea of disjointness. Our approach has two main parts.

**Mining for disjointness**. First, we upgrade the existing parts of the solver to become “disjointness miners.” Their job is to report back whenever they can prove that two tasks cannot overlap. This can be for various reasons:

- Resource clash: like in the puzzle above, two tasks need more of a resource than is available.
- Precedence: task A must finish before task B can start.
- No-good learning: a solver has learned from a previous search round that scheduling tasks C and D together leads to a dead end.

**A `SelectiveDisjunctive` propagator**. Next, we introduce a new `SelectiveDisjunctive` constraint and a propagator for it. While this does not change the set of feasible schedules, you can think of it as a master detective. It takes all the disjointness clues found by the miners and puts them together on a big _conflict graph_. Each task is a node on the graph, and an edge is drawn between any two tasks that are marked as disjoint by miners.

The detective's job is to look for cliques in this graph: groups of tasks where every task is connected to every other task in the group. In our context, any clique is a set of tasks that must all be scheduled sequentially. Once a clique is found, the detective does a quick calculation: it sums up the durations of all tasks in the clique. If that total duration is longer than the available time window for those tasks, it's an “Aha!” moment. The detective has found a conflict, and it tells the solver, “This branch of the search is impossible. Backtrack now!”

Here's an interactive visualization of that process. Each node corresponds to a task that takes a single time unit; the numbers in the node give a time interval available for a task: 1..6 means that a task starts at time 1 or later and finishes at time 6 or earlier. Click the toggles to apply different resource constraints. As you do, you'll see the “disjointness” edges appear. Watch what happens when a clique forms!

<iframe class="iframe-resize" src="{{ '/assets/html/cp2025-clique.html' | relative_url }}" frameborder='0' scrolling='no'></iframe>

This ability to find conflicting cliques by combining information from many different constraints is the superpower of our new approach. It gives the solver a global perspective that it was previously lacking.

## And does it work?

In a word: **yes**!

When we tested our approach on the 3n puzzle that stumped other solvers, ours solved it instantly, and for much larger versions at that. More importantly, when we applied it to well-known, difficult scheduling benchmarks from the research community, we saw some major improvements. On problems with high _resource contention_—meaning resources are scarce and tasks are constantly competing—our approach sometimes improved the solver's speed by **orders of magnitude**. (That means instead of taking hours, it took minutes or even seconds!)

We were also thrilled to discover **new state-of-the-art bounds** for a handful of problems that have been studied by researchers for years. We managed to:
- discover the best-known solutions for two RCPSP/max and four RCPSP instances,
- improve the lower bounds on the achievable objective value for sixteen RCPSP/max and four RCPSP instances,
- and completely solve seven instances that were previously open along the way.

For us, it's like finding a new, faster route through a well-trodden maze.

## The takeaways

The big lesson from our work is that for complex problems, looking at the pieces in isolation isn't enough. By developing ways for the solver to unite information from many sources and reason about the global structure of the problem, we can achieve breakthroughs that were previously out of reach. 

There's still a lot more to explore, but we're excited about this new direction for building smarter and more powerful constraint solvers. Thanks for reading!

