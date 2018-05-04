# sparkmeter_bulk

	Welcome to 'SparkBulk' for set sparkmeter credit or else
	type 'Help <topic>' for more help
	1	Show setting (sparkmeter credentials)
	2	Bulk Zeroing credit balance 	!!!for all meter on current setting!!!
	3	Bulk Set custom credit balance	!!!for all meter on current setting!!!
	4	Change meter state
	5	Change meter tariff
	6	Create payment to change meter credit
	==========================================================================
	l	Login
	f	Set custom filter
	g	Get meter based on custom filter (f) for current login session (l)
	c	Compare current taken meters by (g) with csv (semicolon delimiters) file 
	s	Setting
	x	Exit

=================================================
=================================================
=================================================
===================GUIDE=========================
=================================================
=================================================
create bulk zeroing meter credit 30 april 4pm
	turn all to off
	zeroing credit
	turn all non streetlight to auto
create bulk meter state
create bulk meter reset
	site selection
	infinite run; run-once
	logging all action: who is reset, datetime, meter_serial, customer_name, customer_code
	
= 1 
firstly login--------------- l login
select cloud url------------ 3-13
enter to save session------- ENTER
quit from current step------ x

=== 1.a
get all meter on cloud------ g
select re-state command----- 4
type meter state------------ off

=== 1.b
get all meter on cloud------ g
zeroing credit command------ 6
amount target--------------- 0
current maximum credit val-- 0
execute--------------------- ENTER

=== 1.c
set filter------------------ f fn filter_non_villagelight.json
get all meter on cloud------ g
select re-state command----- 4
type meter state------------ auto

= 2
see step `1`
see step `1.a` for non filtered meters; or
see step `1.c` for set as filtering mode -----> see `f command`

= 3
8 reset-protect
select target site




