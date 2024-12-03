from typing import Dict, Any, List
import pandas as pd
from datetime import datetime, timedelta

class ActionExecutor:
    def __init__(self):
        self.scheduled_actions = []
        self.executed_actions = []
        self.policies = {}
        
    def schedule_action(self, action: Dict[str, Any]) -> bool:
        """Schedule an optimization action"""
        # Validate action against policies
        if not self.validate_action(action):
            return False
        
        # Add scheduling information
        action['scheduled_time'] = datetime.now()
        action['status'] = 'scheduled'
        
        # Add to scheduled actions
        self.scheduled_actions.append(action)
        return True
    
    def execute_scheduled_actions(self) -> List[Dict[str, Any]]:
        """Execute all scheduled actions"""
        results = []
        
        for action in self.scheduled_actions:
            try:
                if action['type'] == 'right_sizing':
                    result = self.execute_sizing_action(action)
                elif action['type'] == 'schedule_scaling':
                    result = self.execute_scaling_action(action)
                elif action['type'] == 'cost_control':
                    result = self.execute_cost_control(action)
                else:
                    result = {'status': 'error', 'message': 'Unknown action type'}
                
                results.append(result)
                self.executed_actions.append({**action, **result})
            except Exception as e:
                results.append({
                    'status': 'error',
                    'message': str(e),
                    'action': action
                })
        
        # Clear scheduled actions
        self.scheduled_actions = []
        return results
    
    def validate_action(self, action: Dict[str, Any]) -> bool:
        """Validate action against policies"""
        # Check if action type is allowed
        if action['type'] not in self.policies.get('allowed_actions', []):
            return False
        
        # Check service-specific policies
        service = action.get('service')
        if service:
            service_policies = self.policies.get(service, {})
            
            # Check cost impact
            if 'max_cost_impact' in service_policies:
                potential_savings = float(action['potential_savings'].replace('$', ''))
                if potential_savings > service_policies['max_cost_impact']:
                    return False
            
            # Check allowed hours
            if 'allowed_hours' in service_policies:
                action_hours = action.get('parameters', {}).get('hours', [])
                if not all(h in service_policies['allowed_hours'] for h in action_hours):
                    return False
        
        return True
    
    def execute_sizing_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a resource sizing action"""
        # This would integrate with cloud provider's API
        return {
            'status': 'simulated',
            'message': f"Would resize {action['service']} from {action['parameters']['current_size']} to {action['parameters']['recommended_size']}",
            'execution_time': datetime.now()
        }
    
    def execute_scaling_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a scaling action"""
        # This would integrate with cloud provider's API
        return {
            'status': 'simulated',
            'message': f"Would scale {action['service']} by factor {action['parameters']['scale_factor']} during hours {action['parameters']['hours']}",
            'execution_time': datetime.now()
        }
    
    def execute_cost_control(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a cost control action"""
        # This would integrate with cloud provider's API
        return {
            'status': 'simulated',
            'message': f"Would set budget alert to ${action['parameters']['budget_threshold']:,.2f} for {action['service']}",
            'execution_time': datetime.now()
        }
    
    def set_policy(self, policy_type: str, policy_config: Dict[str, Any]):
        """Set or update a policy"""
        self.policies[policy_type] = policy_config