#!/usr/bin/perl

		### ParsingAccuracyMeasuresDocLevelForSystems.pl (evaluate discourse trees) computes P, R and F measures of labeled and unlabled constructs.
		### Written by Shafiq R. Joty
		### Date: June, 5 2011

use warnings;
use strict;

use Cwd;
my $cwd = getcwd();
use DTNODE;

my $sysDir = shift;
my $gldDir = shift;
my $outfile = shift;

#data structures to store candidate constituents 
my %doc_edus         = ();
my %doc_spans        = ();
my %doc_nucSpans     = ();
my %doc_relSpans     = ();
my %doc_nucRelSpans  = ();

#data structures to store gold constituents 
my %goldDoc_edus         = ();
my %goldDoc_spans        = ();
my %goldDoc_nucSpans     = ();
my %goldDoc_relSpans     = ();
my %goldDoc_nucRelSpans  = ();

#data structure to store the tree
my @disTree = ();
my $nodeNb  = 0;
my %relation_class = ();

readRelationClasses();
measureMetrics();

sub readRelationClasses{
	open (FILE, "./parsing_eval_metrics/deRelationClasses.txt") || die "Cannot open RelationClasses.txt to read\n";

	while(<FILE>){
		my $line = $_;
		chomp ($line);

		$line =~ s/([\w\-]+)\:\s+//g;
		my $value = $1;
		my @keys   = split /,\s+/, $line;

		foreach my $key (@keys){
			$key =~ s/^\s*//;
			$key =~ s/\s*$//;
			$relation_class{$key} = $value;		
		}
	}
	close (FILE);
}
 
sub measureMetrics{

	opendir DIR,"$sysDir" or die "Can't open $sysDir";
	my @canFiles = grep /\w+\.dis/, readdir(DIR);
	closedir (DIR);
	
	foreach my $sysfile(sort @canFiles){
		#warn "--------------- $sysfile";
		#parse the candidate tree

		@disTree = ();
		$nodeNb  = 0;
		parseDiscouseStr("$sysDir/$sysfile");
		extractCandidateConstructs($sysfile);

		#parse the gold tree
		@disTree = ();
		$nodeNb  = 0;
		my $gldfile = $sysfile;
#		$gldfile =~ s/\.doc_dis/.out.dis/gi; # use this when using the unchanged (multi-nuclears) data
		parseDiscouseStr("$gldDir/$gldfile");
		extractGoldConstructs($sysfile);

		my @list1 = sort (@{$goldDoc_edus{$sysfile}});
		my @list2 = sort (@{$doc_edus{$sysfile}});

		#use this test when using manual segmentation...(joty)
		for (my $i = 0; $i < scalar(@list1); $i++){
			if ($list1[$i] ne $list2[$i]){
				print "ERROR!!!.. the two lists aren't equal ";
				print $list1[$i], " vs ", $list2[$i];
			}		
		} 
	}
	#measure the P, R and F
	computeAccuracy();
}
 
 #----------------------EXTRACT CONSTRUCTS-----------------------------------------
 
 sub extractGoldConstructs{
 
	my $file = shift;
	#exclude root node
	for (my $i = 1; $i < scalar (@disTree); $i++){

		#EDUs	
		if ($disTree[$i]-> getType() eq "leaf"){			
			my $edu_str  = join (":", $disTree[$i]-> getWordSpan());
			$edu_str    .= "_$file";
			push @{$goldDoc_edus{$file}}, $edu_str;
		}
		
		my @Q = ();
		push @Q, $disTree[$i];
		my @wordSpans = ();
		
		#other constructs
		while(scalar (@Q)){
			my $nd = pop @Q;
			if ($nd-> getType() eq "leaf"){
				push @wordSpans, join (":", $nd-> getWordSpan());  
			}
			else{
				push @Q, reverse ($nd-> getChildren());
			}
		}
		
		my @firstWordNb = ($wordSpans[0] =~ m/(\d+):\d+/g);
		my $lastIndex   = scalar(@wordSpans) - 1;
		my @lastWordNb = ($wordSpans[$lastIndex] =~ m/\d+:(\d+)/g);
		if ($disTree[$i]-> getType() ne "leaf"){			
			$disTree[$i]-> setWordSpan($firstWordNb[0], $lastWordNb[0]);
		}
		
		my $span_str     = "Span ". $firstWordNb[0] . ":". $lastWordNb[0]. "_$file";
		my $nuc_str      = $disTree[$i]-> getNuclearity(). " ". $firstWordNb[0] . ":". $lastWordNb[0]. "_$file";
		
		my $rel          = $disTree[$i]-> getRelation();
		$rel             = "\L$rel";
		my $rel_str      = "";		
		if ($relation_class{$rel}){
			$rel_str      = $relation_class{$rel}.   " ". $firstWordNb[0] . ":". $lastWordNb[0]. "_$file"; # handle the relation classes here
		}
		else{
			print "\n ERROR!!! Relation $rel not found";
			my $wt = <STDIN>;	
		}	
		
		push @{$goldDoc_spans{$file}}, $span_str;
		push @{$goldDoc_relSpans{$file}}, $rel_str;
		push @{$goldDoc_nucSpans{$file}}, $nuc_str;
	}
}
 

 sub extractCandidateConstructs{

	my $file = shift;
	# warn scalar (@disTree);
	#exclude root node (as in Marcu'00 book)
	for (my $i = 1; $i < scalar (@disTree); $i++){

		#EDUs	
		if ($disTree[$i]-> getType() eq "leaf"){			
			my $edu_str  = join (":", $disTree[$i]-> getWordSpan());
			$edu_str    .= "_$file";
			push @{$doc_edus{$file}}, $edu_str;
		}
		
		my @Q = ();
		push @Q, $disTree[$i];
		my @wordSpans = ();
		
		#other constructs
		while(scalar (@Q)){
			my $nd = pop @Q;
			if ($nd-> getType() eq "leaf"){
				push @wordSpans, join (":", $nd-> getWordSpan());  
			}
			else{
				push @Q, reverse ($nd-> getChildren());
			}
		}
		
		my @firstWordNb = ($wordSpans[0] =~ m/(\d+):\d+/g);
		my $lastIndex   = scalar(@wordSpans) - 1;
		my @lastWordNb = ($wordSpans[$lastIndex] =~ m/\d+:(\d+)/g);
		if ($disTree[$i]-> getType() ne "leaf"){			
			$disTree[$i]-> setWordSpan($firstWordNb[0], $lastWordNb[0]);
		}
		
		my $span_str     = "Span ". $firstWordNb[0] . ":". $lastWordNb[0]. "_$file";
		my $nuc_str      = $disTree[$i]-> getNuclearity(). " ". $firstWordNb[0] . ":". $lastWordNb[0]. "_$file";
		
		my $rel          = $disTree[$i]-> getRelation();
		$rel             = "\L$rel";
		my $rel_str      = "";		
		if ($relation_class{$rel}){
			$rel_str      = $relation_class{$rel}.   " ". $firstWordNb[0] . ":". $lastWordNb[0]. "_$file"; # handle the relation classes here
		}
		else{
			print "\n ERROR!!! Relation $rel not found";
			my $wt = <STDIN>;	
		}	
		
		push @{$doc_spans{$file}}, $span_str;
		push @{$doc_relSpans{$file}}, $rel_str;
		push @{$doc_nucSpans{$file}}, $nuc_str;
	}
}

#---------------------------------------------------------------------------------------
 
 sub computeAccuracy{
 
	use Set::Scalar;

	my @allCandEDUs   = ();
	my @allGoldEDUs   = ();
	my @allCandSpans  = ();
	my @allGoldSpans  = ();
	my @allCandNuc    = ();
	my @allGoldNuc    = ();
	my @allCandRel    = ();
	my @allGoldRel    = ();

	open (FILE, ">$outfile") || die "Cannot open $outfile to write\n";
	print FILE "Document \t Construct \t Sub2 Card. \t Sub1 Card. \t Com. Card. \t Precision \t Recall \t F-measure";
	print FILE "\n===========================================================================================================";
	
 	foreach my $doc(sort keys %doc_edus){

		#print edus
		push @allCandEDUs,  @{$doc_edus{$doc}};
		push @allGoldEDUs,  @{$goldDoc_edus{$doc}};
		
		my $a = Set::Scalar->new (@{$doc_edus{$doc}});
	    my $b = Set::Scalar->new (@{$goldDoc_edus{$doc}});
		my $i = $a * $b;
		print FILE "\n$doc \t EDU \t\t ", $a->size(), " \t ", $b->size(), " \t ", $i->size();
	    print FILE " \t ", ( $i->size() / $a->size() ) * 100;
	    print FILE " \t ", ( $i->size() / $b->size() ) * 100;
	    print FILE " \t ", (2 * $i->size() ) / ($a->size() + $b->size()) * 100;		
		
		#print spans
		push @allCandSpans, @{$doc_spans{$doc}};
		push @allGoldSpans, @{$goldDoc_spans{$doc}};
		$a = Set::Scalar->new (@{$doc_spans{$doc}});
	    $b = Set::Scalar->new (@{$goldDoc_spans{$doc}});
		$i = $a * $b;
		print FILE "\n$doc \t SPAN \t\t ", $a->size(), " \t ", $b->size(), " \t ", $i->size();
	    print FILE " \t ", ( $i->size() / $a->size() ) * 100;
	    print FILE " \t ", ( $i->size() / $b->size() ) * 100;
	    print FILE " \t ", (2 * $i->size() ) / ($a->size() + $b->size()) * 100;		

		#print Nuclearity
		push @allCandNuc,   @{$doc_nucSpans{$doc}};
		push @allGoldNuc,   @{$goldDoc_nucSpans{$doc}};
		$a = Set::Scalar->new (@{$doc_nucSpans{$doc}});
	    $b = Set::Scalar->new (@{$goldDoc_nucSpans{$doc}});
		$i = $a * $b;
		print FILE "\n$doc \t NUCLEARITY  ", $a->size(), " \t ", $b->size(), " \t ", $i->size();
	    print FILE " \t ", ( $i->size() / $a->size() ) * 100;
	    print FILE " \t ", ( $i->size() / $b->size() ) * 100;
	    print FILE " \t ", (2 * $i->size() ) / ($a->size() + $b->size()) * 100;		


		#print Relation
		push @allCandRel,   @{$doc_relSpans{$doc}};
		push @allGoldRel,   @{$goldDoc_relSpans{$doc}};
		$a = Set::Scalar->new (@{$doc_relSpans{$doc}});
	    $b = Set::Scalar->new (@{$goldDoc_relSpans{$doc}});
		$i = $a * $b;
		print FILE "\n$doc \t RELATION \t ", $a->size(), " \t ", $b->size(), " \t ", $i->size();
	    print FILE " \t ", ( $i->size() / $a->size() ) * 100;
	    print FILE " \t ", ( $i->size() / $b->size() ) * 100;
	    print FILE " \t ", (2 * $i->size() ) / ($a->size() + $b->size()) * 100;		
	    print ", ", (2 * $i->size() ) / ($a->size() + $b->size()) * 100;
		
	}

	print FILE "\n==============================================================================================";
	print FILE "\nSUMMARY OF THE MEASURES";
	print FILE "\nConstruct \t Sub2 Card. \t Sub1 Card. \t Com. Card. \t Precision \t Recall \t F-measure";
	print FILE "\n==============================================================================================";

	#edu
	my $a = Set::Scalar->new (@allCandEDUs);
    my $b = Set::Scalar->new (@allGoldEDUs);
	my $i = $a * $b;
	print FILE "\nEDU \t\t ", $a->size(), " \t ", $b->size(), " \t ", $i->size();
    print FILE " \t ", ( $i->size() / $a->size() ) * 100;
    print FILE " \t ", ( $i->size() / $b->size() ) * 100;

    print FILE " \t ", (2 * $i->size() ) / ($a->size() + $b->size()) * 100;		

	#span
	$a = Set::Scalar->new (@allCandSpans);
    $b = Set::Scalar->new (@allGoldSpans);
	$i = $a * $b;
	print FILE "\nSPAN \t\t ", $a->size(), " \t ", $b->size(), " \t ", $i->size();
    print FILE " \t ", ( $i->size() / $a->size() ) * 100;
    print FILE " \t ", ( $i->size() / $b->size() ) * 100;
    print FILE " \t ", (2 * $i->size() ) / ($a->size() + $b->size()) * 100;		

	#nuclearity
	$a = Set::Scalar->new (@allCandNuc);
    $b = Set::Scalar->new (@allGoldNuc);
	$i = $a * $b;
	print FILE "\nNUCLEARITY \t ", $a->size(), " \t ", $b->size(), " \t ", $i->size();
    print FILE " \t ", ( $i->size() / $a->size() ) * 100;
    print FILE " \t ", ( $i->size() / $b->size() ) * 100;
    print FILE " \t ", (2 * $i->size() ) / ($a->size() + $b->size()) * 100;		
	
	#relation
	$a = Set::Scalar->new (@allCandRel);
    $b = Set::Scalar->new (@allGoldRel);
	$i = $a * $b;
	print FILE "\nRELATION \t ", $a->size(), " \t ", $b->size(), " \t ", $i->size();
    print FILE " \t ", ( $i->size() / $a->size() ) * 100;
    print FILE " \t ", ( $i->size() / $b->size() ) * 100;
    print FILE " \t ", (2 * $i->size() ) / ($a->size() + $b->size()) * 100;		

	close (FILE);
 }


 
  
#----------------------------------- PARSING ---------------------------------------------------------------- 
 
sub parseDiscouseStr{

	my $filePath = shift;
	undef $/;
	# print "\n Parsing $filePath";
	open (FILE1, "$filePath") || die "Cannot open $filePath to read\n";
	
	my $fileContent = <FILE1>;
	$fileContent =~ s/(text _![^\n]*)[()]([^\n]*_!\))/$1 $2/g;

	close (FILE1);
	makeTree($fileContent);
	$/="\n";
	assignWordSpans();	
	# print "\n Parsing done...";
}

#------------------

sub assignWordSpans{
	#assign word spans to edus
	my @Q = ();
	push @Q, $disTree[0]; #insert root
	my $beginWNb = 1;	
	while(scalar (@Q)){
		my $nd = pop @Q;
		if ($nd-> getType() eq "leaf"){
			my $edu_str = $nd-> getText();

			#needed to compare tokenized text.
			$edu_str    =~ s/\-LHB\-/(/g;
			$edu_str    =~ s/\-RHB\-/)/g;
			$nd-> setText($edu_str);

			$edu_str    = handlePunctions($edu_str);

			#changed the following two lines to deal with tokenized str.
#			my @words   = (split / /, $edu_str);
#			my $endWNb  = $beginWNb + scalar (@words) - 1;

			my $endWNb  = $beginWNb + length ($edu_str) - 1;
	
			$nd-> setWordSpan($beginWNb, $endWNb);
			$beginWNb = $endWNb + 1;	
		}
		else{
			push @Q, reverse ($nd-> getChildren());
		}
	}
}

#------------------

sub makeTree{

	my $str = shift;
	removeBoundary(\$str);

	my $rootStr = "";
	extractRoot(\$str, \$rootStr);
	 
	#create a root node
	$disTree[$nodeNb] = new DTNODE($nodeNb);
	populateNodeValues($rootStr, $nodeNb);
	$nodeNb++;

	#Get the substrings
	my @subStrs = (); 
	getSubStrings($str, \@subStrs);

	#create that many children
	createChildren($disTree[$nodeNb -1], \@subStrs);

	while(1){
		my $node = traverseTree();

		if ($node == 0){
			last;
		}
		my $str = $node-> getText();
		removeBoundary(\$str);
		my $root = "";
		extractRoot(\$str, \$root);
		populateNodeValues($root, $node-> getNodeNb());
		if ($str =~ m/\w+/){
			my @subStrs = ();
			getSubStrings($str, \@subStrs);
			createChildren($node, \@subStrs); 
		}	
	}
}

#---------------------------------------------------------------------------
sub getSubStrings{

	my $str = shift;
	my $subStrs = shift;
	#find the distinct constructs 
	my @symbols = ($str=~ m/(\n\s+\( | \)|\n\s+\)|.+\S\))/g);
	
	my $left  = 0;
	my $right = 0;
	my $begin = 0;

	for (my $i=0; $i< scalar(@symbols);$i++){
		if($symbols[$i] =~ m/\n\s+\( /){
			$left++;
		}
		if($symbols[$i] =~ m/( \)|\n\s+\))/){
			$right++;
		}
		if($left == $right){
			my $end = $i;
			my $temp = join("",(@symbols[$begin .. $end]));
			push @{$subStrs}, $temp;
			$begin = $i+1;
		}
	}
}


#--------------------------------------------------------------------------

sub traverseTree{
	my @Q = ();
	push @Q, $disTree[0];
	while(scalar (@Q)){
		my $nd = shift @Q;
		if($nd-> getFlag() == 0){
			return $nd;
		}
		else{
			push @Q, $nd-> getChildren();
		}	
	}	
	return 0;
}

#--------------------------------------------------------------------------
sub createChildren{
	my $parent = shift;
	my $subStrs = shift;	
	#creating the nodes 
	foreach my $st(@$subStrs){
		#make a dummy node with null values and the substr (raw) got.
		$disTree[$nodeNb] = new DTNODE($nodeNb);
		$disTree[$nodeNb] -> setText($st);
		$disTree[$nodeNb] -> setParent($parent);
		$parent-> pushChild($disTree[$nodeNb]);
		$nodeNb++;
	}	
}

#create a node from the given string
sub populateNodeValues{
	my $nodeStr = shift;
	my $nodeNb  = shift;	

	#take nuclearity and type
	my @nuc_type = ($nodeStr =~ m/^(\w+) \((\w+) /g);

	if (scalar (@nuc_type)){
		$disTree[$nodeNb]-> setNuclearity($nuc_type[0]);
		$disTree[$nodeNb]-> setType($nuc_type[1]);
		
		#take span range and edu id and text
		if ($nuc_type[1] eq "span"){
			my @span_range = ($nodeStr =~ m/^\w+ \(\w+ (\d+) (\d+)\)/g);
			$disTree[$nodeNb]-> setSpanRange(@span_range);
		}		
		elsif ($nuc_type[1] eq "leaf"){
			my @eduId = ($nodeStr =~ m/\(leaf (\d+)\)/g);
			$disTree[$nodeNb]-> setEDUId($eduId[0]);

			my @text = 	($nodeStr =~ m/\(text _!(.+)_!\)/g);
	        $disTree[$nodeNb]-> setText($text[0]);
		}
		else{
			print "\n PARSING ERROR!! node type not found..";
			my $wt = <STDIN>;
		}
		
		#take relation	
		if ($nuc_type[0] ne "Root"){
			my @rel = ($nodeStr =~ m/\(rel2par ([^)]+)\)/g);
			$disTree[$nodeNb]-> setRelation($rel[0]);
#			$relations{$rel[0]} = 1;
		}
		$disTree[$nodeNb]-> setFlag();
	}
	else{
		print "\n PARSING ERROR!! node creation..";
		my $wt = <STDIN>;
	}	
}

#remove the first word from the string  
sub extractRoot{
	my $st = shift;
	my $root = shift;
	if ($$st =~ m/^\w+\s+\(leaf\s+\d+\)/) {
		$$st =~ s/^(.+_!\))//; 
		$$root = $1;
		
	} else {
		$$st =~ s/^(.+\S\))//;
		$$root = $1;
	}
}
#remove the first and last bracket 
sub removeBoundary{
	my $st = shift;
	$$st =~ s/^\s*\(\s*//;
	$$st =~ s/\s*$//;
	$$st =~ s/\s*\)\s*$// unless $$st =~ /_!\)$/;
}


sub handlePunctions{
	my $str = shift;
 	$str =~ s/(``|'')/"/gi;
 	$str =~ s/(`|')/'/gi;
 	$str =~ s/-LHB-/(/gi;
 	$str =~ s/-RHB-/)/gi;
	$str =~ s/\s//gi;
	#don't exclude <P> for doc-level 
	return $str;
}
