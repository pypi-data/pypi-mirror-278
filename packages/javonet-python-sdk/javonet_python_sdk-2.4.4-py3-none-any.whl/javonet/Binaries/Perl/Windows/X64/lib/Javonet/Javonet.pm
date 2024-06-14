package Javonet::Javonet;
use strict;
use warnings FATAL => 'all';
use Moose;
use lib 'lib';
use aliased 'Javonet::Sdk::Internal::RuntimeFactory' => 'RuntimeFactory';
use aliased 'Javonet::Core::Transmitter::PerlTransmitter' => 'Transmitter', qw(activate_with_license_file activate_with_credentials activate_with_credentials_and_proxy);

BEGIN {
    Transmitter->activate_with_license_file()
}

sub activate {
    if(@_ == 1) {
        return Transmitter->activate_with_license_file();
    }
    if(@_ == 2) {
        my($self, $licenseKey) = @_;
        return Transmitter->activate_with_credentials($licenseKey);
    } elsif (@_ > 2) {
        my($self, $licenseKey, $proxyHost, $proxyUserName, $proxyPassword) = @_;
        $proxyUserName //="";
        $proxyPassword //="";
        return Transmitter->activate_with_credentials_and_proxy($licenseKey, $proxyHost, $proxyUserName, $proxyPassword);
    }

}

sub in_memory {
    return RuntimeFactory->new(Javonet::Sdk::Internal::ConnectionType::get_connection_type('InMemory'), undef, undef);
}

sub tcp {
    # additional shift is needed to pass second argument
    my $class = shift;
    my $address = shift;
    return RuntimeFactory->new(Javonet::Sdk::Internal::ConnectionType::get_connection_type('Tcp'), $address, undef);
}

sub with_config {
    my ($self, $config_path) = @_;
    # Sets the configuration source
    Transmitter->set_config_source($config_path);
    # Returns a new RuntimeFactory instance configured with a custom configuration file
    return RuntimeFactory->new(Javonet::Sdk::Internal::ConnectionType::get_connection_type('WithConfig'), undef, $config_path);
}

1;