#!/usr/bin/env python3
"""
Decision Engine - Accept/Continue/Reject logic with context assurance
"""

from enum import Enum
from typing import Tuple, Optional

class Decision(Enum):
    ACCEPT = "ACCEPT"
    CONTINUE = "CONTINUE"
    REJECT = "REJECT"

class DecisionEngine:
    def __init__(self):
        """Initialize decision engine"""
        self.accept_threshold = 0.80  # 80%
        self.continue_threshold = 0.60  # 60%
        self.context_loss_threshold = 0.40  # 40% context loss
        self.max_iterations = 5
    
    def context_maintained(self, current_score: float, previous_score: Optional[float]) -> bool:
        """Check if context is maintained between iterations"""
        if previous_score is None:
            return True  # First iteration, no previous context
        
        # Calculate context loss
        context_loss = abs(current_score - previous_score) / previous_score if previous_score > 0 else 1.0
        
        # Context is maintained if loss is below threshold
        return context_loss <= self.context_loss_threshold
    
    def context_degradation_detected(self, current_score: float, previous_score: Optional[float]) -> bool:
        """Detect if context has degraded significantly"""
        if previous_score is None:
            return False
        
        # Significant degradation: score dropped by more than 40%
        degradation = (previous_score - current_score) / previous_score if previous_score > 0 else 0.0
        return degradation > self.context_loss_threshold
    
    def make_decision(self, score: float, previous_score: Optional[float], 
                     iteration: int, chunk_type: str = "") -> Tuple[Decision, str]:
        """
        Make decision based on score, previous score, and iteration
        
        Returns: (Decision, reason)
        """
        # Check for context degradation
        if self.context_degradation_detected(score, previous_score):
            return (Decision.REJECT, f"Context degradation detected: {score:.2%} vs {previous_score:.2%}")
        
        # ACCEPT: Score ≥80% + context maintained
        if score >= self.accept_threshold:
            if self.context_maintained(score, previous_score):
                return (Decision.ACCEPT, f"High score ({score:.2%}) with context maintained")
            else:
                # High score but context not maintained - continue to verify
                if iteration < self.max_iterations:
                    return (Decision.CONTINUE, f"High score ({score:.2%}) but context check needed")
                else:
                    return (Decision.ACCEPT, f"High score ({score:.2%}) - final iteration")
        
        # CONTINUE: Score 60-79% + iterations remaining
        elif score >= self.continue_threshold:
            if iteration < self.max_iterations:
                return (Decision.CONTINUE, f"Medium score ({score:.2%}) - continue to iteration {iteration + 1}")
            else:
                # Last iteration, accept if context maintained
                if self.context_maintained(score, previous_score):
                    return (Decision.ACCEPT, f"Medium score ({score:.2%}) - final iteration, context maintained")
                else:
                    return (Decision.REJECT, f"Medium score ({score:.2%}) - final iteration, context lost")
        
        # REJECT: Score <60% OR context loss >40%
        else:
            if self.context_maintained(score, previous_score):
                # Low score but context maintained - might continue if early iteration
                if iteration < 3:  # Early iterations, give more chances
                    return (Decision.CONTINUE, f"Low score ({score:.2%}) but early iteration, continue")
                else:
                    return (Decision.REJECT, f"Low score ({score:.2%}) - insufficient match")
            else:
                return (Decision.REJECT, f"Low score ({score:.2%}) and context loss detected")
    
    def should_exit(self, iteration: int, all_processed: bool, 
                   no_improvable_chunks: bool) -> bool:
        """Check if we should exit the recursive loop"""
        # Exit conditions:
        # 1. All chunks processed and scored
        if all_processed:
            return True
        
        # 2. Maximum iterations reached
        if iteration >= self.max_iterations:
            return True
        
        # 3. No improvable chunks remaining
        if no_improvable_chunks:
            return True
        
        return False
    
    def get_next_iteration_strategy(self, decision: Decision, iteration: int, 
                                   chunk_type: str) -> str:
        """Get strategy for next iteration based on decision"""
        if decision == Decision.ACCEPT:
            return "output_token"
        elif decision == Decision.CONTINUE:
            # Determine next iteration strategy
            if iteration == 1:
                return "phrase_breakdown"
            elif iteration == 2:
                return "verb_object_pairs"
            elif iteration == 3:
                return "individual_words"
            elif iteration == 4:
                return "final_resolution"
            else:
                return "force_best_match"
        else:  # REJECT
            return "skip_chunk"

def main():
    """Test decision engine"""
    engine = DecisionEngine()
    
    # Test cases
    test_cases = [
        (0.85, None, 1, "High score, first iteration"),
        (0.75, 0.80, 2, "Medium score, context maintained"),
        (0.55, 0.60, 3, "Low score, context maintained"),
        (0.30, 0.80, 4, "Low score, context degraded"),
        (0.65, 0.70, 5, "Medium score, final iteration"),
    ]
    
    print("Decision Engine - Test Cases")
    print("=" * 80)
    
    for score, prev_score, iteration, description in test_cases:
        decision, reason = engine.make_decision(score, prev_score, iteration)
        strategy = engine.get_next_iteration_strategy(decision, iteration, "")
        print(f"\n{description}:")
        print(f"  Score: {score:.2%}, Previous: {prev_score:.2% if prev_score else 'N/A'}, Iteration: {iteration}")
        print(f"  Decision: {decision.value}")
        print(f"  Reason: {reason}")
        print(f"  Strategy: {strategy}")

if __name__ == "__main__":
    main()

