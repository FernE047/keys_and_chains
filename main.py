import time
from typing import Literal

ChainTypes = Literal["Chain", "Key"]


class Chain:
    category: ChainTypes

    def __init__(
        self,
        category: ChainTypes,
        content: "list[Chain]|None" = None,
        visualizations: set[str] | None = None,
    ) -> None:
        self.category = category
        if content is None:
            self.content: list[Chain] = []
        else:
            self.content = content
        if visualizations is None:
            self.visualizations: set[str] = set()
        else:
            self.visualizations = visualizations
        self.visualizations.add(str(self))
        self.has_all_vis = False

    def copy(self) -> "Chain":
        new_content: list[Chain] = [chain.copy() for chain in self.content]
        chain = Chain(self.category, new_content, self.visualizations.copy())
        return chain

    def rotate(self) -> "Chain":
        new_chain = self.copy()
        new_chain.content.append(new_chain.content.pop(0))
        new_chain.visualizations.add(str(new_chain))
        return new_chain

    def enter(self) -> "Chain":
        if not self.content:
            return self.copy()
        new_chain = self.content[0].copy()
        old_chain = self.copy()
        old_chain.content.pop(0)
        new_chain.content.append(old_chain)
        new_chain.visualizations = self.visualizations.copy()
        new_chain.visualizations.add(str(new_chain))
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

    def list_visualizations(self) -> str:
        text = ""
        vis_sort = sorted(self.visualizations)
        for n, vis in enumerate(vis_sort):
            text += f"    {n + 1}. `{vis}`\n"
        return text

    def find_all_visualizations(self) -> None:
        if self.has_all_vis:
            return
        stack: list[Chain] = [self]
        while stack:
            chain = stack.pop(0)
            enter_chain = chain.enter()
            if not chain.content:
                continue
            if str(enter_chain) not in self.visualizations:
                self.visualizations.add(str(enter_chain))
                stack.append(enter_chain)
            if chain.category == "Key":
                continue
            if len(chain.content) <= 1:
                continue
            rotate_chain = chain.rotate()
            if str(rotate_chain) not in self.visualizations:
                self.visualizations.add(str(rotate_chain))
                stack.append(rotate_chain)
        self.has_all_vis = True

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Chain):
            raise NotImplementedError("only comparable with chains")
        if self.has_all_vis:
            return str(other) in self.visualizations
        elif other.has_all_vis:
            return str(self) in other.visualizations
        else:
            self.find_all_visualizations()
            return str(other) in self.visualizations

    def unique_str(self) -> str:
        self.find_all_visualizations()
        vis_sort = sorted(self.visualizations, reverse=True)
        return str(vis_sort[0])

    def __hash__(self) -> int:
        return hash(self.unique_str())

    def add_key(self) -> "Chain":
        self.content.append(Chain("Key"))
        self.visualizations = {str(self)}
        return self


def convert_it(text: str, index:int) -> tuple[Chain, int]:
    chain = Chain("Chain")
    char = text[index]
    if char == "[":
        chain.category = "Chain"
    elif char == "(":
        chain.category = "Key"
    index += 1
    text_size = len(text)
    while index < text_size:
        char = text[index]
        if char == ",":
            index += 1
            continue
        if char in ["[", "("]:
            new_chain, index = convert_it(text, index)
            chain.content.append(new_chain)
            index += 1
            continue
        chain.visualizations = {str(chain)}
        return chain, index
    chain.visualizations = {str(chain)}
    return chain, index


def convert_text_to_chain(text: str) -> Chain:
    chain, _ = convert_it(text, 0)
    return chain


if __name__ == "__main__":
    begin = time.time()
    initial_chains = [
        convert_text_to_chain("[[[]]]"),
    ]
    with open("output.md", "w") as file:
        previous_chains: list[Chain] = []
        for n, chain in enumerate(initial_chains):
            file.write(f"{n + 1}. `{chain}`\n")
            chain.find_all_visualizations()
            file.write(chain.list_visualizations() + "\n")
            previous_chains.extend(
                [convert_text_to_chain(vis) for vis in chain.visualizations]
            )
        for level in range(10):
            file.write(f"## KEY {level + 1}\n\n")
            all_chains: set[Chain] = set()
            for chain in previous_chains:
                if chain.category == "Key":
                    continue
                all_chains.add(chain.add_key())
            previous_chains: list[Chain] = []
            print(f"{level + 1} : {len(all_chains)}")
            for n, chain in enumerate(all_chains):
                file.write(f"{n + 1}. `{chain.unique_str()}`\n")
                chain.find_all_visualizations()
                # file.write(chain.list_visualizations() + "\n")
                if len(all_chains) > 5000:
                    continue
                for vis in chain.visualizations:
                    sub_chain = convert_text_to_chain(vis)
                    if sub_chain.category == "Key":
                        continue
                    previous_chains.append(sub_chain)
            file.write("\n")
            if len(all_chains) > 5000:
                break
    end = time.time()
    print(end - begin)
