class QueryFormatter:
    @classmethod
    def wrap(cls, val: str | int | float, extra: str = "") -> str:
        if type(val) == str or val is None: return f"'{extra}{val}{extra}'"
        else: return val
    
    @classmethod
    def method_field(cls, field: str, val: str, method: str) -> list[str]:
        return [
            f"{field} like {QueryFormatter.wrap(val, '%')}" * (bool(val) and (method == "like")),
            f"{field} = {QueryFormatter.wrap(val)}"         * (bool(val) and (method == "exact")),
        ]

    @classmethod
    def equal_field(cls, field: str, val: str) -> list[str]:
        return [
            f"{field} = {QueryFormatter.wrap(val)}" * bool(val)
        ]   

    @classmethod
    def in_field(cls, field: str, val: str) -> list[str]:
        val = val or []
        return [
            f"{field} in ({','.join([QueryFormatter.wrap(v) for v in val])})" * bool(val)
        ]   

    @classmethod
    def m_atk_def_field(cls, field: str, val: str) -> str:   
        val = (val or '').replace(' ', '')  

        if not val:
            return [ "" ]

        if val.isdigit():
            return [ f"{field} = {val}" * bool(val) ]

        if max(val.count('>'), val.count('<'), val.count('=')) == 1:
            return [ f"{field} {val}" * bool(val) ]

        if max(val.count('>'), val.count('<'), val.count('=')) > 1:
            first_val = "" # 100
            first_compare = "" # <=
            # something like "x" in between
            second_compare = "" # <
            second_val = "" # 1000
            
            left_half = True
            for c in val:
                if c.isdigit():
                    if left_half: first_val += c
                    else: second_val += c
                if c.isalpha():
                    left_half = False
                if not (c.isdigit() or c.isalpha()):
                    if left_half: first_compare += c
                    else: second_compare += c

            return [ f"{field} {first_compare} {first_val} AND {field} {second_compare} {second_val}" * bool(val) ]

        return [ "" ]