"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """Encapsulates access to the input code. Reads and assembly language 
    command, parses it, and provides convenient access to the commands 
    components (fields and symbols). In addition, removes all white space and 
    comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        input_lines = input_file.read().splitlines()
        valid_input_lines = []
        # remove white spaces:
        for line in input_lines:
            new_line = ''.join(line.split())
            ind = new_line.find("//")
            if ind != (-1):
                valid_input_lines.append(new_line[0:ind])
            else:
                valid_input_lines.append(new_line)
        input_lines = [line for line in valid_input_lines if line != ""]

        self._input_lines = input_lines
        self._num_of_lines = len(input_lines)
        self._curr_index = 0


    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        # Your code goes here!
        return self._curr_index <= self._num_of_lines - 1

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        # Your code goes here!
        self._curr_index += 1


    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        # Your code goes here!
        command = self._input_lines[self._curr_index]
        if command[0] == "@":
            return "A_COMMAND"
        elif command[0] == "(":
            return "L_COMMAND"
        else:
            return "C_COMMAND"

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or 
            "L_COMMAND".
        """
        # Your code goes here!

        if self.command_type() == "A_COMMAND":
            return self._input_lines[self._curr_index][1:]
        else:  # L_COMMAND
            return self._input_lines[self._curr_index][1:-1]

    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        command = self._input_lines[self._curr_index]
        start_ind = 0
        end_ind = command.find("=")
        if end_ind != -1:
            return command[start_ind:end_ind]
        return ""

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        command = self._input_lines[self._curr_index]
        start_ind = 0
        temp = command.find("=")
        if temp != -1:
            start_ind = temp + 1
        temp = command.find(";")
        if temp != -1:
            end_ind = temp
            return command[start_ind:end_ind]
        return command[start_ind:]

    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        command = self._input_lines[self._curr_index]
        start_ind = command.find(";")
        if start_ind != -1:
            return command[start_ind + 1:]
        return ""
