<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<CodeBlocks_project_file>
	<FileVersion major="1" minor="6" />
	<Project>
		<Option title="{{project_name}}" />
		<Option makefile_is_custom="1" />
		<Option pch_mode="2" />
		<Option compiler="gcc" />
		<MakeCommands>
			<Build command="{{zhixin_path}} -f -c codeblocks run" />
			<CompileFile command="{{zhixin_path}} -f -c codeblocks run" />
			<Clean command="{{zhixin_path}} -f -c codeblocks run -t clean" />
			<DistClean command="{{zhixin_path}} -f -c codeblocks run -t clean" />
			<AskRebuildNeeded command="1" />
			<SilentBuild command="{{zhixin_path}} -f -c codeblocks run &gt; $(CMD_NULL)" />
		</MakeCommands>
		<Build>
			<Target title="Debug">
				<Option type="4" />
				<Option compiler="gcc" />
				<Option parameters="-f -c codeblocks run -t upload" />
				<Option host_application="{{zhixin_path}}" />
				<Option run_host_application_in_terminal="1" />
				<Option use_console_runner="0" />
				<MakeCommands>
					<Build command="{{zhixin_path}} -f -c codeblocks run" />
					<CompileFile command="{{zhixin_path}} -f -c codeblocks run" />
					<Clean command="{{zhixin_path}} -f -c codeblocks run -t clean" />
					<DistClean command="{{zhixin_path}} -f -c codeblocks run -t clean" />
					<AskRebuildNeeded command="1" />
					<SilentBuild command="{{zhixin_path}} -f -c codeblocks run &gt; $(CMD_NULL)" />
				</MakeCommands>
			</Target>
			<Target title="Release">
				<Option type="4" />
				<Option compiler="gcc" />
				<Option parameters="-f -c codeblocks run -t upload" />
				<Option host_application="{{zhixin_path}}" />
				<Option run_host_application_in_terminal="1" />
				<Option use_console_runner="0" />
				<MakeCommands>
					<Build command="{{zhixin_path}} -f -c codeblocks run" />
					<CompileFile command="{{zhixin_path}} -f -c codeblocks run" />
					<Clean command="{{zhixin_path}} -f -c codeblocks run -t clean" />
					<DistClean command="{{zhixin_path}} -f -c codeblocks run -t clean" />
					<AskRebuildNeeded command="1" />
					<SilentBuild command="{{zhixin_path}} -f -c codeblocks run &gt; $(CMD_NULL)" />
				</MakeCommands>
			</Target>
		</Build>
		<Compiler>
			% for define in defines:
			<Add option="-D{{define}}"/>
			% end
			% for include in filter_includes(includes):
			<Add directory="{{include}}"/>
			% end
		</Compiler>
		<Unit filename="zhixin.ini" />
		% for file in src_files:
		<Unit filename="{{file}}"></Unit>
		% end
	</Project>
</CodeBlocks_project_file>
