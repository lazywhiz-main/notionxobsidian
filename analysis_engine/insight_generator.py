from typing import List, Dict, Any

class InsightGenerator:
    def __init__(self):
        pass

    def generate_related_content_insights(self, analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        insights = []
        if "similarities" in analysis_results:
            for i, row in enumerate(analysis_results["similarities"]):
                for j, sim in enumerate(row):
                    if i < j and sim > 0.7: # Example threshold
                        insights.append({
                            "type": "related_content",
                            "content_a_id": analysis_results["content_ids"][i],
                            "content_b_id": analysis_results["content_ids"][j],
                            "similarity_score": sim,
                            "message": f"Content '{analysis_results['content_ids'][i]}' and '{analysis_results['content_ids'][j]}' are highly related."
                        })
        return insights

    def generate_duplicate_insights(self, analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        insights = []
        if "duplicates" in analysis_results:
            for dup in analysis_results["duplicates"]:
                insights.append({
                    "type": "duplicate_content",
                    "content_a_id": analysis_results["content_ids"][dup["index_a"]],
                    "content_b_id": analysis_results["content_ids"][dup["index_b"]],
                    "similarity_score": dup["similarity"],
                    "message": f"Potential duplicate detected between '{analysis_results['content_ids'][dup['index_a']]}' and '{analysis_results['content_ids'][dup['index_b']]}'. Consider merging."
                })
        return insights

    def generate_summary_insight(self, content_id: str, summary_text: str) -> Dict[str, Any]:
        return {
            "type": "summary",
            "content_id": content_id,
            "summary": summary_text,
            "message": f"Summary for '{content_id}': {summary_text[:100]}..."
        }

    def generate_action_recommendation(self, insight: Dict[str, Any]) -> Dict[str, Any]:
        if insight["type"] == "duplicate_content":
            return {
                "action_type": "merge_content",
                "target_ids": [insight["content_a_id"], insight["content_b_id"]],
                "description": insight["message"] + " Please review and merge."
            }
        elif insight["type"] == "related_content":
            return {
                "action_type": "link_content",
                "target_ids": [insight["content_a_id"], insight["content_b_id"]],
                "description": insight["message"] + " Consider creating a link."
            }
        return {"action_type": "review", "target_ids": [insight.get("content_id", "N/A")], "description": insight["message"]}