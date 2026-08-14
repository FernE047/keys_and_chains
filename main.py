from typing import Literal

ChainTypes = Literal["Chain", "Key"]


class Chain:
    category: ChainTypes

    def __init__(
        self,
        category: ChainTypes,
        content: "list[Chain]|str|None" = None,
        visualizations: set[str] | None = None,
    ) -> None:
        self.category = category
        if content is None:
            self.content: list[Chain] = []
        elif isinstance(content, str):
            self.content = convert_text_to_chain(content).content
        else:
            self.content = content
        if visualizations is None:
            self.visualizations: set[str] = set()
        else:
            self.visualizations = visualizations
        self.add_visualization(self)

    def link(self, content: "Chain") -> None:
        self.content.append(content)
        self.visualizations = set()
        self.add_visualization(self)

    def add_visualization(self, chain: "Chain") -> None:
        self.visualizations.add(str(chain))

    def copy_visualizations(self, chain: "Chain") -> None:
        self.visualizations = chain.visualizations.copy()

    def copy(self) -> "Chain":
        new_content: list[Chain] = [chain.copy() for chain in self.content]
        chain = Chain(self.category, new_content, self.visualizations.copy())
        return chain

    def rotate(self) -> "Chain":
        if self.category == "Key":
            return self.copy()
        if len(self.content) <= 1:
            return self.copy()
        new_chain = self.copy()
        new_chain.content.append(new_chain.content.pop(0))
        new_chain.add_visualization(new_chain)
        return new_chain

    def enter(self) -> "Chain":
        if not self.content:
            return self.copy()
        new_chain = self.content[0].copy()
        old_chain = self.copy()
        old_chain.content.pop(0)
        new_chain.content.append(old_chain)
        new_chain.copy_visualizations(self)
        new_chain.add_visualization(new_chain)
        return new_chain

    def __str__(self) -> str:
        text = ""
        if self.category == "Chain":
            text += "["
        else:
            text += "("
        if self.content:
            sub_chains: list[str] = []
            for chain in self.content:
                sub_chains.append(str(chain))
            text += ",".join(sub_chains)
        if self.category == "Chain":
            text += "]"
        else:
            text += ")"
        return text

    def print_visualizations(self) -> None:
        vis_sort = sorted(self.visualizations)
        for n, vis in enumerate(vis_sort):
            print(f"    {n + 1}. `{vis}`")

    def find_all_visualizations(self) -> None:
        stack: list[Chain] = [self]
        while stack:
            chain = stack.pop(0)
            rotate_chain = chain.rotate()
            if str(rotate_chain) not in self.visualizations:
                self.add_visualization(rotate_chain)
                stack.append(rotate_chain)
            enter_chain = chain.enter()
            if str(enter_chain) not in self.visualizations:
                self.add_visualization(enter_chain)
                stack.append(enter_chain)


def convert_text_to_chain(text: str | list[str]) -> Chain:
    chain = Chain("Chain")
    if isinstance(text, str):
        chars = list(text)
    else:
        chars = text
    char = chars.pop(0)
    closure = ""
    if char == "[":
        chain.category = "Chain"
        closure = "]"
    elif char == "(":
        chain.category = "Key"
        closure = ")"
    while chars:
        if chars[0] in ["[", "("]:
            chain.link(convert_text_to_chain(chars))
            continue
        char = chars.pop(0)
        if char == ",":
            continue
        if char == closure:
            return chain
    return chain


if __name__ == "__main__":
    chains = [
        "[[[(),()]]]",
        "[[[()],()]]",
        "[[[],(),()]]",
        "[[[()]],()]",
        "([[],(),[]])",
        "([[[],()]])",
    ]
    for m,chain_text in enumerate(chains):
        print(f"{m+1}. `{chain_text}`")
        chain = convert_text_to_chain(chain_text)
        chain.find_all_visualizations()
        chain.print_visualizations()
        print()
