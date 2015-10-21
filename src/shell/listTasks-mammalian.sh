#!/bin/bash
DIR_DISTIQUE=$WS_HOME/DISTIQUE/src/shell
DIR_NJst=$WS_HOME/ASTRID/src
DIR_Astral=$WS_HOME/ASTRAL/Astral
path_mammalian=/oasis/projects/nsf/uot136/esayyari/data/BSfiles
DIR_UTILS=$WS_HOME/DISTIQUE/src/utils
method=prod
summethod=fm
out=/oasis/projects/nsf/uot136/esayyari/outputs/

if [ -s $DIR/tasks.massive ]; then
rm $DIR/tasks.massive
fi

path_tmp=$path_mammalian
for file in `find $path_tmp -type f -name "*.bs"`; do
	tmp_out=$( dirname "${file}" )
	tmp_out=$( echo $tmp_out | sed -e "s/^.*data\///" )
	f_tmp=$( basename "${file}" )
	fout=$(echo $f_tmp | sed -e 's/\.bs//g')
	echo $fout
	if [ -d $out/$tmp_out/$fout/distique-2/$method ]; then
		printf "the folder $out/$tmp_out/$fout/distique-2/$method already exists\n"
	else
		printf "the folder $out/$tmp_out/$fout/distique-2/$method created\n"
		mkdir -p $out/$tmp_out/$fout/distique-2/$method
	fi
	if [ -d $out/$tmp_out/$fout/astral ]; then
		printf "the folder $out/$tmp_out/$fout/astral already exists\n"
	else
		printf "the folder $out/$tmp_out/$fout/astral created\n"
		mkdir -p $out/$tmp_out/$fout/astral
	fi
	if [ -d $out/$tmp_out/$fout/njst ]; then
		printf "the folder $out/$tmp_out/$fout/njst already exists\n"
	else
		printf "the folder $out/$tmp_out/$fout/njst created\n"
		mkdir -p $out/$tmp_out/$fout/njst
	fi
	if [ ! -s $out/$tmp_out/$fout/astral/distance.d_astral_tree.nwk ]; then 
	printf "mkdir -p ./$out/$tmp_out/$fout/astral;  /usr/bin/time -po ./$out/$tmp_out/$fout/astral/$f_tmp-log.info java -Xmx2000M -jar $DIR_Astral/astral.4.7.8.jar -i $file -o ./$out/$tmp_out/$fout/astral/distance.d_astral_tree.nwk; mv ./$out/$tmp_out/$fout/astral $out/$tmp_out/$fout/astral\n">>tasks.massive
	fi
#if [ ! -s $out/$tmp_out/distique-cons/$method/$method/distance.d_distique_tree.nwk ]; then
#		printf "mkdir -p ./$out/$tmp_out/distique-cons/$method/; source /etc/profile.d/modules.sh; module load python; module load scipy; VIRTUAL_ENV_DISABLE_PROMPT=1; source $WS_HOME/python27-gordon/bin/activate; /usr/bin/time -po ./$out/$tmp_out/distique-cons/$mehtod/$f_tmp-log.info $DIR_UTILS/distique.py -g $file -m $method  -o ./$out/$tmp_out/distique-cons/$method -x 2; cp -r ./$out/$tmp_out/distique-cons/$method $out/$tmp_out/distique-cons/$method\n">>tasks.massive-$method.8
#	fi
	if [ ! -s $out/$tmp_out/$fout/distique-2/$method/distance.d_distique_tree.nwk ]; then
		printf "mkdir -p ./$out/$tmp_out/$fout/distique-2/$method/; source /etc/profile.d/modules.sh; module load python; module load scipy; VIRTUAL_ENV_DISABLE_PROMPT=1; source $WS_HOME/python27-gordon/bin/activate; /usr/bin/time -po ./$out/$tmp_out/$fout/distique-2/$mehtod/$f_tmp-log.info $DIR_UTILS/distique-2.py -g $file -m $method  -o ./$out/$tmp_out/$fout/distique-2/$method -x 2; cp -r ./$out/$tmp_out/$fout/distique-2/$method $out/$tmp_out/$fout/distique-2/$method\n">>tasks.massive
	fi
	if [ ! -s $out/$tmp_out/distance.d_njst_tree.nwk ]; then
	printf "mkdir -p ./$out/$tmp_out/$fout/njst source /etc/profile.d/modules.sh; module load python; module load scipy; VIRTUAL_ENV_DISABLE_PROMPT=1; source $WS_HOME/python27-gordon/bin/activate; /usr/bin/time -po ./$out/$tmp_out/$fout/njst/$f_tmp-log.info python $DIR_NJst/ASTRID.py -i $file -m fastme2 -o ./$out/$tmp_out/$fout/njst/distance.d_njst_tree.nwk -c ./$out/$tmp_out/$fout/njst/CACHE.csv; mv ./$out/$tmp_out/$fout/njst $out/$tmp_out/$fout/njst \n" >>tasks.massive
	fi
done
