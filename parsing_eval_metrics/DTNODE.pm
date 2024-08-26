    #Discourse tree node attributes and methods

use warnings;
package DTNODE;

	$nodeNb     = -1; # node number in the tree

	$spanRange  = []; # edu ids for span
	$eduId      = 0;  # EDU id for leaves
	$relation   = ""; # span or relation   
	$text       = ""; # text if type is leaf	
	$type       = ""; # span or leaf
	$nuclearity = ""; # nuc or sat or root 
	$flag       =  0; # processed or not 
	
	$parent     = -1; # parent id 
	$children   = []; # children
	$sibling    = ""; # sibling
	$wordSpanRange  = []; #  word ids for span
	


# constructor 

	sub new{
		my $class = shift;		
		my $nb    = shift;
		my $self = {};
		
		$self->{nodeNb}    = $nb;
		$self->{spanRange} = [];
		$self->{eduId}     = 0;
		$self->{relation}  = "";
		$self->{text}      = "";
		$self->{type}      = "";
		$self->{nuclearity}= "";
		$self->{flag}      = 0;
		$self->{parent}    = -1;
		$self->{children}  = [];
		$self->{sibling}   = "";
		
		bless $self, $class;
	}
	
	sub getNodeNb{
		my $self = shift;
		return $self->{nodeNb};
	}

	sub setNuclearity{
		my $self = shift;
		$self->{nuclearity} = shift;
	}
	sub getNuclearity{
		my $self = shift;
		return $self->{nuclearity};
	}
	
	sub setType{
		my $self = shift;
		$self->{type} = shift;
	}

	sub getType{
		my $self = shift;
		return $self->{type};
	}

	
	sub setEDUId{
		my $self = shift;
		$self->{eduId} = shift;
	}

	sub getEDUId{
		my $self = shift;
		return $self->{eduId};
	}

	sub setFlag{
		my $self = shift;
		$self->{flag} = 1;
	}
	
	sub getFlag{
		my $self = shift;
		return $self->{flag};
	}

	sub setParent{
		my $self = shift;
		$self->{parent} = shift;
	}

	sub getParent{
		my $self = shift;
		return $self->{parent};
	}

	sub pushChild{
		my $self  = shift;
		my $chld  = shift;
		push @{$self->{children}}, $chld;
	}
	
	sub getChildren{
		my $self = shift;
		return @{$self->{children}};
	}
	
	sub assignSibling{
		my $self  = shift;
		my $sib  = shift;
		$self->{sibling} = $sib;
	}
	
	sub getSibling{
		my $self = shift;
		return $self->{sibling};
	}
	
	sub setSpanRange{
		my $self = shift;
		my @span = @_;
		@{$self->{spanRange}} = @span;
	}
	
	sub setWordSpan{
		my $self = shift;
		my @span = @_;
		@{$self->{wordSpanRange}} = @span;
	}

	sub getWordSpan{
		my $self = shift;
		return @{$self->{wordSpanRange}};
	}
	
	sub getSpanRange{
		my $self = shift;
		return @{$self->{spanRange}};
	}
	
	sub setRelation{
		my $self = shift;
		$self->{relation} = shift;
	}	
	
	sub getRelation{
		my $self = shift;
		return $self->{relation};
	}	
	
	sub setText{
		my $self = shift;
		$self->{text} = shift;
	}	

	sub getText{
		my $self = shift;
		return $self->{text};
	}

1;
