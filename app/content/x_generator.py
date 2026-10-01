def generate_x_post(asset: str, risk: dict, analysis: dict) -> str:
    text = f"{asset} market state: {risk['level']} risk ({risk['score']}/100). {analysis['narrative']} Research only, not investment advice."
    return text[:280]
